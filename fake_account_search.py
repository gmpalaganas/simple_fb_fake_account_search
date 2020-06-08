import asyncio
import aiohttp

suspected_fake_ids = []

async def get_response(url):
    resp_code = 404
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                resp_code = response.status
    except Exception as e:
        print(e)
        resp_code = -1

    return resp_code

async def main(base_url, user_id, range_start, range_end):

    range_start = range_start
    range_end = range_end

    test_ids = [ "{}.{}".format(user_id,i) for i in range(range_start,range_end+1) ]


    test_ids_response = await asyncio.gather(*[get_response(base_url+test_id) for test_id in test_ids])
    for i, status in enumerate(test_ids_response):
        if test_ids_response[i] == 200:
            suspected_fake_ids.append(test_ids[i])

try:
    input_file = open("input.txt", "r")
    output_file = open("output.txt","w+")

    base_url = "https://www.facebook.com/"

    lines = input_file.read().splitlines()
    
    user_id = lines[0] 
    range_start = lines[1]
    range_end= lines[2]

    print("ID to be tested is {} with range {} to {}".format(user_id,range_start,range_end))

    loop = asyncio.get_event_loop()

    loop.run_until_complete(main(base_url,user_id,range_start,range_end))

    for suspected_fake_id in suspected_fake_ids:
       output_file.write(base_url + suspected_fake_id + "\n")
    
    input_file.close()
    output_file.close()

    print("Search complete, {} suspected IDs found, please check output.txt for more information".format(len(suspected_fake_ids)))
    input("Press enter key to continue...")

except FileNotFoundError:
    print("Input file does not exist")

