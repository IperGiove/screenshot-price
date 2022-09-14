import plotter
import downloader
import uploader
import asyncio

if __name__ == "__main__":
    data = asyncio.run(downloader.main())
    print(data.head())
    plotter.main(data)
    uploader.main()