#!flask/bin/python
################################################################################################################################
#------------------------------------------------------------------------------------------------------------------------------                                                                                                                             
# This file implements the REST layer. It uses flask micro framework for server implementation. Calls from front end reaches 
# here as json and being branched out to each projects. Basic level of validation is also being done in this file. #                                                                                                                                  	       
#-------------------------------------------------------------------------------------------------------------------------------                                                                                                                              
################################################################################################################################
from flask import Flask, jsonify, abort, request, make_response, url_for,redirect, render_template
from flask_httpauth import HTTPBasicAuth
from werkzeug.utils import secure_filename
import os
import shutil 
import numpy as np
from search import recommend
import tarfile
from datetime import datetime
from scipy import ndimage
#from scipy.misc import imsave
# 文件上传文件夹
UPLOAD_FOLDER = 'uploads'
# 文件扩展名
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
from tensorflow.python.platform import gfile
# 创建flask应用并配置静态url
app = Flask(__name__, static_url_path = "")
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
auth = HTTPBasicAuth()

#==============================================================================================================================
#                                                                                                                              
#    Loading the extracted feature vectors for image retrieval                                                                 
#                                                                          						        
#                                                                                                                              
#==============================================================================================================================
extracted_features=np.zeros((1000,2048),dtype=np.float32)
with open('saved_features_recom.txt') as f:
    		for i,line in enumerate(f):
        		extracted_features[i,:]=line.split()
print("loaded extracted_features") 


#==============================================================================================================================
#                                                                                                                              
#  This function is used to do the image search/image retrieval
#                                                                                                                              
#==============================================================================================================================

#检验是否在文件扩展名中
def allowed_file(filename):
   return '.' in filename and \
          filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
# 查找是否在tag文件中
def check_in_txt(filename,num):
    count=0
    with open(filename,'r')as f:
        for line in f:
            for word in line.split():
                if word.isdigit()and int(word)==num:
                    return True
                count+=1
                if count>=3000:
                     return False
    return False
#特征标签
feature_tags=['sky', 'clouds', 'water', 'sea', 'river', 'lake', 'people', 'portrait',
'male', 'female', 'baby', 'night', 'plant_life', 'tree', 'flower', 'animals',
'dog', 'bird', 'structures', 'sunset', 'indoor', 'transport', 'car']
#查找标签
def find_tag(img_path):
    import os
    import re
    current_path=os.getcwd().replace('\\','/')
    # print(current_path)
    feature=[]
    img_index=re.search(r'\d+',img_path)
    if img_index:
        img_num=int(img_index.group())
    for tag_name in feature_tags:
        filename=current_path+'/database/tags/'+tag_name+'.txt'
        # inputloc = os.path.join("database/tags", tag_name)
        # filename=inputloc+'.txt'
        if check_in_txt(filename,img_num)==True:
            feature.append(tag_name)
    return feature
def check_in_like(img_name):
     if img_name in like_status:
          return True
     else:
          return False
@app.route('/api/imgUpload', methods=['GET', 'POST'])
def upload_img():
    isError=True
    msg=""
    print("image upload")
    #结果文件夹
    result = 'static/result'
    if not gfile.Exists(result):
          os.mkdir(result)
    #清除结果文件夹
    shutil.rmtree(result)
    if request.method == 'POST' or request.method == 'GET':
        print(request.method)
        # check if the post request has the file part
        #请求中没有文件则重定向到原始url
        # if 'file' not in request.files:
        #     print('No file part')
        #     return redirect(request.url)
        
        # file = request.files['file']
        # print(file.filename)
        # if user does not select file, browser also
        # submit a empty part without filename
        # if file.filename == '':
           
        #     print('No selected file')
        #     return redirect(request.url)
        filename = request.get_json().get('info').get('filename','')
        queryNumber = request.get_json().get('info').get('queryNumber',0)
        print(queryNumber)
        print(filename)
        # print(type(queryNumber))
        # if filename == '':
        #     print('No selected file')
        #     return redirect(request.url)
        if allowed_file(filename):
            isError=False
            print(isError)
        else:
            isError=True
            print(isError)
            msg="not allow"
        if 'filename' in request.form:# and allowed_file(file.filename):
            #确保文件名安全
            # filename = secure_filename(filename)
            # #将文件上传到指定文件夹
            # file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            #构造上传文件的完整路径
            inputloc = os.path.join("database\dataset", filename)
            print(inputloc)
            #图像搜索
            recommend(inputloc, extracted_features,queryNumber)
            os.remove(inputloc)
            image_path = "/result"
            #文件名
            img_names=[os.path.basename(file)for file in os.listdir(result)
                              if not file.startswith('.')]
            #文件路径
            image_list =[os.path.join(image_path, file) for file in os.listdir(result)
                              if not file.startswith('.')]
            print(result)
            #tag
            img_tags=[]
            img_likes=[]
            for i in range(len(image_list)):
                 img_tags.append(find_tag(image_list[i]))
                 img_likes.append(check_in_like(img_names[i]))
            print(img_tags)
            print(img_likes)
            tags={f'tag{i}':img_tags[i] for i in range(len(img_tags))}
            all_tags=[]
            for sublist in img_tags:
                 for tag in sublist:
                      all_tags.append(tag)
            unique_tags=list(set(all_tags))
            # images = {
			# 'image0':image_list[0],
            # 'image1':image_list[1],	
			# 'image2':image_list[2],	
			# 'image3':image_list[3],	
			# 'image4':image_list[4],	
			# 'image5':image_list[5],	
			# 'image6':image_list[6],	
			# 'image7':image_list[7],	
			# 'image8':image_list[8]
		    #   }			
            response={
                response:{"isError": isError,
                "msg": msg,
                "data": {
                     "like":check_in_like(filename),
                     "tags":unique_tags,
                    "list": [
                        {
                            "filename": img_name,
                            "isCollected": img_like,
                            "tags": img_tag
                        }for img_name, img_like, img_tag in zip(img_names, img_likes, img_tags)
                    ]
                }}
            }
            # result.update({"all_tags":unique_tags})
            return jsonify(response)
#加入收藏
like_status = []
@app.route('/api/likeImage', methods=['GET', 'POST'])
def like_image():
    print(1)
    response = {
        "isError": True,
        "msg": "",
    }
    data = request.get_json()
    filename = data.get('info').get('filename','')
    like = data.get('like',0)
    print(filename)

    if not filename:
        response["msg"] = "Filename is required."
        return jsonify(response)
    if like is not None:
        if not isinstance(like, int):
            response["msg"] = "Like value must be an integer."
            return jsonify(response)
        if like==1:
            if filename not in like_status:
                like_status.append(filename)
                response["isError"] = False
                response["msg"] = "Operation successful."   
            else:
                 response["msg"] = 'already liked'
        if like==0:
            if filename in like_status:
                like_status.remove(filename)
                response["isError"] = False
                response["msg"] = "Operation successful."   
            else:
                response["msg"] = 'not yet liked'
    print(like_status) 
    return jsonify(response)
#获取收藏
@app.route('/api/getAllLikes', methods=['GET', 'POST'])
def get_all_likes():
    response={
        response:{"isError": True,
        "msg": "",
        "data": {
        "list": [
            {
            }
        ]
        }}
    }
    img_tags=[]
    print(len(like_status))
    for i in range(len(like_status)):
        print(i)
        tags=find_tag(like_status[i])
        response["data"]["list"].append({
        "filename": like_status[i],
        "isCollected": "1",  # 因为这里是获取所有已 like 的图片，状态都为已 like
        "tags": tags
        })
    response['msg']="success"
    response['isError']=False
    return jsonify(response)
@app.route('/api/testPost', methods=['POST'])
def testPost():
    print("get post")
    print(request)
    data = request.form
    age = data.get('age')
    print("Received age:", age)
    return jsonify({'msg':'GET POST'})
#==============================================================================================================================
#                                                                                                                              
#                                           Main function                                                        	            #						     									       
#  				                                                                                                
#==============================================================================================================================
@app.route("/")
def main():
    
    return render_template("main.html")   
if __name__ == '__main__':
    app.run(debug = True, host= '0.0.0.0')
