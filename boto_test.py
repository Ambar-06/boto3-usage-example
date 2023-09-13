import boto3
import secrets
import os
import asyncio

def s3_content_type(file_name):
    try:
        extension = os.path.splitext(file_name)[1].lstrip('.')
        switcher = {
            'png': "image/png",
            'gif': "image/gif",
            'html': "text/html",
            'htmls': "text/html",
            'htm': "text/html",
            'jpg': "image/jpeg",
            'jpeg': "image/jpeg",
            'jfif': "image/jpeg",
            'pdf': "application/pdf",
            'webp': "image/webp",
            'mp4': "video/mp4"
        }
        return switcher.get(extension, "application/octet-stream")
    except Exception as e:
        print(e)

async def upload_to_s3(file_paths):
    image_path_array = []
    s3 = boto3.client(
        's3',
        aws_access_key_id="xxxxx",
        aws_secret_access_key="xxxxx"
    )
    
    for file_path in file_paths:
        try:
            with open(file_path, 'rb') as image_file:
                image_data = image_file.read()

            content_type = s3_content_type(file_path)
            hex_token = secrets.token_hex(16)
            directory = f'test/medias3/social/{hex_token}_{os.path.basename(file_path)}'
            s3.put_object(Bucket='xxxx', Key=directory, Body=image_data, ContentType=content_type)
            image_url = f"https://xxxx.s3.amazonaws.com/{directory}"
            print(image_url)
            image_path_array.append(image_url)
        except FileNotFoundError:
            print(f"File not found: {file_path}")
        except Exception as e:
            print(f"An error occurred while reading {file_path}: {str(e)}")
    
    return image_path_array

file_paths = [
    'C:/Users/LENOVO/Desktop/RandomProjects/boto test/1.jpg',
    'C:/Users/LENOVO/Desktop/RandomProjects/boto test/2.jpg',
    'C:/Users/LENOVO/Desktop/RandomProjects/boto test/3.jfif',
    'C:/Users/LENOVO/Desktop/RandomProjects/boto test/5.jpg',
    'C:/Users/LENOVO/Desktop/RandomProjects/boto test/demo.png'
]

result = asyncio.run(upload_to_s3(file_paths))
print(result)
