import re
import json
# import urllib.request
import os

from requests import get
# from .collection_util import as_tuple
# import lxml
from bs4 import BeautifulSoup

CACHE_PATH = 'assets/posters.json'

if os.path.isfile(CACHE_PATH):
    with open(CACHE_PATH, 'r', encoding='utf-8') as file:
        CACHE = json.load(file)
else:
    CACHE = {}

# MLOOK_PROGRAMMABLE_SEARCH_ENGINE_IDS = os.environ['MLOOK_PROGRAMMABLE_SEARCH_ENGINE_IDS']
# MLOOK_PROGRAMMABLE_SEARCH_ENGINE_API_KEY = os.environ['MLOOK_PROGRAMMABLE_SEARCH_ENGINE_API_KEY']
#
# n_engine_ids = len(MLOOK_PROGRAMMABLE_SEARCH_ENGINE_IDS)
# current_engine_id = 0


# @as_tuple
# def search(query: str):
#     global current_engine_id
#
#     # print(query)
#     response = get(
#         # 'https://www.googleapis.com/customsearch/v1/siterestrict',
#         'https://www.googleapis.com/customsearch/v1',
#         params = {
#             'cx': MLOOK_PROGRAMMABLE_SEARCH_ENGINE_IDS[current_engine_id],
#             'key': MLOOK_PROGRAMMABLE_SEARCH_ENGINE_API_KEY,
#             'q': query,
#             'searchType': 'image'
#         }
#     )
#
#     # print(response.json())
#
#     match (code := response.status_code):
#         case 200:
#             items = response.json().get('items')
#             if items is None:
#                 yield {
#                     'title': query,
#                     'link': None,
#                     'source': 'unsplash.it',
#                     'thumbnail': None,
#                     'original': 'https://unsplash.it/600/400'
#                 }
#             else:
#                 for image in items:
#                     image_image = image.get('image')
#                     yield {
#                         'title': image.get('title'),
#                         'link': None if image_image is None else image_image['contextLink'],
#                         'source': image.get('displayLink'),
#                         'thumbnail': None if image_image is None else image_image['thumbnailLink'],
#                         'original': image.get('link')
#                     }
#         # case 429:
#         #     if current_engine_id < n_engine_ids - 1:
#         #         current_engine_id += 1
#         #         print(f'Switching to the api key with index {current_engine_id}')
#         #         return search(query)
#         #     else:
#         #         raise ValueError(f'Exhausted resources of all api keys')
#         case _:
#             print(response.json())
#             raise ValueError(f'Invalid response code: {code}')

def search(query: str):
    if (result := CACHE.get(query)):
        return result, None

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.114 Safari/537.36",
    }

    if (cookie := os.environ.get('COOKIE')) is None:
        print('cookies are not set')
    else:
        headers["Cookie"] = cookie

    params = {
        "q": query,                   # search query
        "tbm": "isch",                # image results
        # "hl": "en",                   # language of the search
        # "gl": "us",                   # country where search comes from
        "ijn": "0"                    # page number
    }
    html = get("https://www.google.com/search", params=params, headers=headers, timeout=30)
    soup = BeautifulSoup(html.text, "lxml")

    google_images = []

    all_script_tags = soup.select("script")

    # # https://regex101.com/r/48UZhY/4
    matched_images_data = "".join(re.findall(r"AF_initDataCallback\(([^<]+)\);", str(all_script_tags)))

    matched_images_data_fix = json.dumps(matched_images_data)
    matched_images_data_json = json.loads(matched_images_data_fix)

    # https://regex101.com/r/VPz7f2/1
    matched_google_image_data = re.findall(r'\"b-GRID_STATE0\"(.*)sideChannel:\s?{}}', matched_images_data_json)

    # https://regex101.com/r/NnRg27/1
    matched_google_images_thumbnails = ", ".join(
        re.findall(r'\[\"(https\:\/\/encrypted-tbn0\.gstatic\.com\/images\?.*?)\",\d+,\d+\]',
                   str(matched_google_image_data))).split(", ")

    thumbnails = [
        bytes(bytes(thumbnail, "ascii").decode("unicode-escape"), "ascii").decode("unicode-escape") for thumbnail in matched_google_images_thumbnails
    ]

    # removing previously matched thumbnails for easier full resolution image matches.
    removed_matched_google_images_thumbnails = re.sub(
        r'\[\"(https\:\/\/encrypted-tbn0\.gstatic\.com\/images\?.*?)\",\d+,\d+\]', "", str(matched_google_image_data))

    # https://regex101.com/r/fXjfb1/4
    # https://stackoverflow.com/a/19821774/15164646
    matched_google_full_resolution_images = re.findall(r"(?:'|,),\[\"(https:|http.*?)\",\d+,\d+\]", removed_matched_google_images_thumbnails)

    full_res_images = [
        bytes(bytes(img, "ascii").decode("unicode-escape"), "ascii").decode("unicode-escape") for img in matched_google_full_resolution_images
    ]

    for index, (metadata, thumbnail, original) in enumerate(zip(soup.select('.isv-r.PNCib.MSM1fd.BUooTd'), thumbnails, full_res_images), start=1):
        selected = metadata.select_one(".VFACy.kGQAp.sMi44c.lNHeqe.WGvvNb")
        meta_selected = metadata.select_one(".fxgdke")

        google_images.append({
            "title": None if selected is None else selected.get("title"),
            "link": None if selected is None else selected.get("href"),
            "source": None if meta_selected is None else meta_selected.text,
            "thumbnail": thumbnail,
            "original": original
        })

        # Download original images
        # print(f'Downloading {index} image...')

        # opener = urllib.request.build_opener()
        # opener.addheaders = [('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36')]
        # urllib.request.install_opener(opener)

        # urllib.request.urlretrieve(original, f'Bs4_Images/original_size_img_{index}.jpg')

    CACHE[query] = google_images

    with open(CACHE_PATH, 'w', encoding = 'utf-8') as _file:
        json.dump(CACHE, _file)

    return google_images, html.text


# def get_images_with_request_headers():
#     del params["ijn"]
#     params["content-type"] = "image/png" # parameter that indicate the original media type
#
#     return [img["src"] for img in soup.select("img")]
#
# def get_suggested_search_data():
#     suggested_searches = []
#
#     all_script_tags = soup.select("script")
#
#     # https://regex101.com/r/48UZhY/6
#     matched_images = "".join(re.findall(r"AF_initDataCallback\(({key: 'ds:1'.*?)\);</script>", str(all_script_tags)))
#
#     # https://kodlogs.com/34776/json-decoder-jsondecodeerror-expecting-property-name-enclosed-in-double-quotes
#     # if you try to json.loads() without json.dumps it will throw an error:
#     # "Expecting property name enclosed in double quotes"
#     matched_images_data_fix = json.dumps(matched_images)
#     matched_images_data_json = json.loads(matched_images_data_fix)
#
#     # search for only suggested search thumbnails related
#     # https://regex101.com/r/ITluak/2
#     suggested_search_thumbnails = ",".join(re.findall(r'{key(.*?)\[null,\"Size\"', matched_images_data_json))
#
#     # https://regex101.com/r/MyNLUk/1
#     suggested_search_thumbnail_encoded = re.findall(r'\"(https:\/\/encrypted.*?)\"', suggested_search_thumbnails)
#
#     for suggested_search, suggested_search_fixed_thumbnail in zip(soup.select(".PKhmud.sc-it.tzVsfd"), suggested_search_thumbnail_encoded):
#         suggested_searches.append({
#             "name": suggested_search.select_one(".VlHyHc").text,
#             "link": f"https://www.google.com{suggested_search.a['href']}",
#             # https://regex101.com/r/y51ZoC/1
#             "chips": "".join(re.findall(r"&chips=(.*?)&", suggested_search.a["href"])),
#             # https://stackoverflow.com/a/4004439/15164646 comment by Frédéric Hamidi
#             "thumbnail": bytes(suggested_search_fixed_thumbnail, "ascii").decode("unicode-escape")
#         })
#
#     return suggested_searches

# def get_original_images():
#
#     """
#     https://kodlogs.com/34776/json-decoder-jsondecodeerror-expecting-property-name-enclosed-in-double-quotes
#     if you try to json.loads() without json.dumps() it will throw an error:
#     "Expecting property name enclosed in double quotes"
#     """
#
#     google_images = []
#
#     all_script_tags = soup.select("script")
#
#     # # https://regex101.com/r/48UZhY/4
#     matched_images_data = "".join(re.findall(r"AF_initDataCallback\(([^<]+)\);", str(all_script_tags)))
#
#     matched_images_data_fix = json.dumps(matched_images_data)
#     matched_images_data_json = json.loads(matched_images_data_fix)
#
#     # https://regex101.com/r/VPz7f2/1
#     matched_google_image_data = re.findall(r'\"b-GRID_STATE0\"(.*)sideChannel:\s?{}}', matched_images_data_json)
#
#     # https://regex101.com/r/NnRg27/1
#     matched_google_images_thumbnails = ", ".join(
#         re.findall(r'\[\"(https\:\/\/encrypted-tbn0\.gstatic\.com\/images\?.*?)\",\d+,\d+\]',
#                    str(matched_google_image_data))).split(", ")
#
#     thumbnails = [
#         bytes(bytes(thumbnail, "ascii").decode("unicode-escape"), "ascii").decode("unicode-escape") for thumbnail in matched_google_images_thumbnails
#     ]
#
#     # removing previously matched thumbnails for easier full resolution image matches.
#     removed_matched_google_images_thumbnails = re.sub(
#         r'\[\"(https\:\/\/encrypted-tbn0\.gstatic\.com\/images\?.*?)\",\d+,\d+\]', "", str(matched_google_image_data))
#
#     # https://regex101.com/r/fXjfb1/4
#     # https://stackoverflow.com/a/19821774/15164646
#     matched_google_full_resolution_images = re.findall(r"(?:'|,),\[\"(https:|http.*?)\",\d+,\d+\]", removed_matched_google_images_thumbnails)
#
#     full_res_images = [
#         bytes(bytes(img, "ascii").decode("unicode-escape"), "ascii").decode("unicode-escape") for img in matched_google_full_resolution_images
#     ]
#
#     for index, (metadata, thumbnail, original) in enumerate(zip(soup.select('.isv-r.PNCib.MSM1fd.BUooTd'), thumbnails, full_res_images), start=1):
#         google_images.append({
#             "title": metadata.select_one(".VFACy.kGQAp.sMi44c.lNHeqe.WGvvNb")["title"],
#             "link": metadata.select_one(".VFACy.kGQAp.sMi44c.lNHeqe.WGvvNb")["href"],
#             "source": metadata.select_one(".fxgdke").text,
#             "thumbnail": thumbnail,
#             "original": original
#         })
#
#         # Download original images
#         print(f'Downloading {index} image...')
#
#         opener=urllib.request.build_opener()
#         opener.addheaders=[('User-Agent','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36')]
#         urllib.request.install_opener(opener)
#
#         urllib.request.urlretrieve(original, f'Bs4_Images/original_size_img_{index}.jpg')
#
#     return google_images
