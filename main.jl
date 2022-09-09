using HTTP
using JSON
import YAML
using DataFrames
using PlotlyJS
using Dates


const DATA = YAML.load_file("config.yaml", dicttype=Dict{String, Any})
const DATE = Dates.format(Dates.now(), "yyyy-mm-dd HH:MM:SS")

"""
Make http request and parse
"""
function requests_and_parse(;
    url::String, 
    header::Dict = Dict("Content-Type" => "application/json"), 
    http_method::String = "GET", 
    query::Union{Dict, Nothing} = nothing
    ) 
    
    r = HTTP.request(http_method, url, header=header, query=query)
    return JSON.Parser.parse(String(r.body)), r.status
end


function params_for_request(exchange::String, quot::String, base::String) :: Tuple{String, Union{Dict, Nothing}}
    pair = quot * DATA[exchange]["pairs_merge"] * base

    if isnothing(DATA[exchange]["query"])
        query = nothing
        url = DATA[exchange]["host"] * DATA[exchange]["price"]["endpoint"] * pair
    else
        query = Dict(DATA[exchange]["query"] => pair)
        url = DATA[exchange]["host"] * DATA[exchange]["price"]["endpoint"]
    end

    return url, query
end


function convert_to_float(non_float) :: Float64
    if typeof(non_float) != Float64
        return parse(Float64, non_float)
    end
    return non_float
end


function preprocessing(exchange::String, row_data::Union{Dict, Vector}) :: Float64
    if isnothing(DATA[exchange]["where_data"])
        return round(
            convert_to_float(row_data[DATA[exchange]["price"]["price_data"]]),
            digits=2
        )
    else
        return round(
            convert_to_float(row_data[DATA[exchange]["where_data"]][DATA[exchange]["price"]["price_data"]]), 
            digits=2
        )
    end
end


function get_price() :: DataFrame
    df = DataFrame(Dict(
        "exchange" => [],
        "pair" => [],
        "price" => []
    ))
    
    for exchange in DATA["exchanges"], 
        quot in DATA["pairs"]["quote"], 
        base in DATA["pairs"]["base"]

        url, query = params_for_request(exchange, quot, base)
        row_data, status = requests_and_parse(url=url, query=query)
        price_data = preprocessing(exchange, row_data)

        push!(df, (exchange, quot*base, price_data))

    end

    return sort!(df, [:price])
end


function make_plot(df)
    fig = plot(
        df, 
        x = :exchange, 
        y = :price, 
        kind = "bar",
        text = :price,
        texttemplate="%{text:.2s}",
        textposition="inside",
        marker = attr(
            showscale = true, 
            coloraxis = "coloraxis", 
            color = :price
        ),
        Layout(
            width = 800,
            height = 200,
            yaxis_type = "log",
            font = attr(size = 16, color=:white), 
            paper_bgcolor = :black, 
            plot_bgcolor = :black,
            title = attr(text = "BTCEUR Arbitrage Opportunity at $DATE", xanchor = "left"),
            margin = attr(b = 0, r = 0, t = 45, l = 0)
        )
    )
    savefig(fig, "BTCEUR.png", width = 800, height = 200)
end


function main()
    df = get_price()
    make_plot(df)
    println(df)
end


if abspath(PROGRAM_FILE) == @__FILE__
    main()
end