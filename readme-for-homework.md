# 1. Environment
Please download **requirement.txt** and enter `conda create --name <env> --file <this file>` in cmd.
Replace *env* with your conda environment name and *this file* with *requirement.txt*.
# 2. Usage
## + Backend
  1. Download the code provided by the teacher. Unzip the package.
  2. Open **lab3-image-retrieval\lab2-image-retrieval\server\database\tags_LAPTOP-JPAR2S4C_3月-25-144331-2022_conflict_parent**.Copy all the files in it to **lab3-image-retrieval\lab2-image-retrieval\server\database\tags**.
  3. Use our file **backend_picRetrieval** of the same name to replace the following files in the unpacked installation package:  

    - image_vectorizer.py  
    - rest-server.py  
    - search.py
  4. Run `image_vectorizer.py` and generate image_list.pickle and saved_features.txt.
  5. Run `rest-server.py`.
## + Frontend
1. Open our file **frontend_picRetrieval\search**.
2. Copy the dataset folder provided by the teacher to this path: frontend_picRetrieval\search\src\assets, **put the 'dataset' folder into folder 'assets'!!**
3. Run `npm install` and `npm run dev`.
4. Open the URL: http://localhost:5173/ and you can use the website.