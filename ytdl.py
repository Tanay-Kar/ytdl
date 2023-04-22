from ytdownloader import YoutubeDownloader,YoutubeDownloaderException
from colorama import Fore, Back, Style, init
import os
import json

class CLIWrapper:
    def __init__(self, downloader: YoutubeDownloader):

        init(autoreset=True)
        self.downloader = downloader
        if self.downloader.apptype != "CLI":
            self.downloader.apptype = "CLI"
        print()
        self.print_details()
        print()
        self.choose_resolution()

    def choose_resolution(self):
        print(Fore.CYAN + Style.BRIGHT + "Available Resolutions:")
        index = []
        for i, e in enumerate(self.downloader.res_list):
            print(f"{i+1}.", Fore.YELLOW + Style.BRIGHT + f"{e}")
            index.append(i+1)
        choice = int(input(Fore.GREEN + Style.BRIGHT +
                     f"Enter your choice ({''.join([str(i)+',' for i in index])[:-1]}): " + Style.RESET_ALL))
        while choice not in index:
            choice = int(input(Fore.GREEN + Style.BRIGHT +
                         f"Enter your choice from the list ({''.join([str(i)+',' for i in index])[:-1]}): " + Style.RESET_ALL))
        choice = self.downloader.res_list[choice-1]
        print()
        default_loc = os.path.join(os.path.expanduser("~"), "Downloads")
        loc_choice = input(Fore.GREEN + Style.BRIGHT +
                           f"Enter location to save the file (default: {default_loc}): " + Style.RESET_ALL)
        while not (loc_choice == "" or os.path.isdir(loc_choice)):
            loc_choice = input(Fore.GREEN + Style.BRIGHT +
                               f"Enter correct location to save the file (default: {default_loc}): " + Style.RESET_ALL)
        loc_choice = loc_choice if loc_choice != "" else default_loc
        print()
        print(Fore.CYAN + Style.BRIGHT + "Downloading..." + Style.RESET_ALL)
        print('\n' + Fore.RED + Style.BRIGHT +
              "Press Ctrl+C to stop the download.\n\n")
        self.downloader.download(choice, loc_choice)

    def print_details(self):

        url, title, channel, duration, _, res_list = self.downloader.url, self.downloader.title, self.downloader.channel, self.downloader.duration, self.downloader.thumbnail, self.downloader.res_list
        print(Style.BRIGHT + Fore.YELLOW + "URL: ", Fore.CYAN + f"{url}")
        print(Style.BRIGHT + Fore.YELLOW + "Title:", Style.BRIGHT + f"{title}")
        print(Style.BRIGHT + Fore.YELLOW +
              "Channel:", Style.BRIGHT + f"{channel}")
        print(Style.BRIGHT + Fore.YELLOW + "Duration:",
              Style.BRIGHT + f"{duration}")
        print(Style.BRIGHT + Fore.YELLOW + "Available Resolutions:",
              Style.BRIGHT + f"{res_list}")


class RESPONSEWrapper:
    def __init__(self, downloader: YoutubeDownloader, query="DQ", res=None, loc=None):

        self.downloader = downloader
        self.query = query  # DQ for details query, RQ for resolution query, D for download
        if self.downloader.apptype != "RESPONSE":
            self.downloader.apptype = "RESPONSE"

        if self.query == "DQ":
            self.print_details()
        elif self.query == "RQ":
            _, _, _, _, _, res_list = self.downloader.get_details()
            response = {}
            response['type'] = 'RESOLUTION QUERY'
            response['res_list'] = res_list
            print(json.dumps(response, indent=4))
        elif self.query == "D":
            self.downloader.download(res, loc)
        else:
            raise Exception("Invalid query type")

    def print_details(self):

        url, title, channel, duration, _, res_list = self.downloader.url, self.downloader.title, self.downloader.channel, self.downloader.duration, self.downloader.thumbnail, self.downloader.res_list
        response = {}
        response['type'] = 'DETAIL QUERY'
        response['url'] = url
        response['title'] = title
        response['channel'] = channel
        response['duration'] = duration
        response['res_list'] = res_list

        print(json.dumps(response, indent=4))


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('url', help='Youtube URL')
    parser.add_argument('-v', '--verbose',
                        help='Verbose mode', action='store_true')
    parser.add_argument('-t', '--type', help='CLI type [R - Response, C - CLI]',
                        choices=['R', 'C'], default='C')
    parser.add_argument('-q', '--query', help='Query type [DQ - Details Query, RQ - Resolution Query, D - Download]',
                        choices=['DQ', 'RQ', 'D'])
    parser.add_argument('-r', '--resolution', help='Resolution to download')
    parser.add_argument('-l', '--location', help='Location to save the file')

    args = parser.parse_args()
    verbose = args.verbose

    url = args.url
    apptype = args.type
    query = args.query
    res = args.resolution
    loc = args.location

    if apptype == 'C':
        print('Ignoring all other switches except verbosity')
    elif apptype == 'R' and query == None:
        raise Exception("Query type is required")
    elif apptype == 'R' and query == 'D':
        if res is None:
            raise Exception("Resolution is required")
        if loc == None:
            print('Location is not provided. Using default download location')
            loc = os.path.join(os.path.expanduser("~"), "Downloads")

    try:
        if apptype == 'C':
            wrapper = CLIWrapper(YoutubeDownloader(
                args.url, apptype="CLI", verbose=verbose))
        else:
            wrapper = RESPONSEWrapper(YoutubeDownloader(
                args.url, apptype="RESPONSE", verbose=verbose), query, res, loc)

        print('\n'*6 if not verbose else '\n'*2)
        print(Fore.GREEN + Style.BRIGHT +
              "Thank you for using" + Style.RESET_ALL)

    except KeyboardInterrupt:
        print()
        print('Quiting ...')
    except Exception as e:
        print()
        print(e)
        
