
#
from flask import Flask,render_template,request,redirect, url_for                     
import pickle
import uuid
import os


app = Flask(__name__)


   
#--------------------------------------------------------------------------------------------------------------

@app.route ('/', methods =['POST','GET'])
def index():
    try:
        # คำสั่งเปิดไฟล์เพื่ออ่าน
        with open('static/item.txt', 'rb') as h:
            # คำสั่งโหลดข้อมูล
            items = pickle.load(h)
    except:
        items = []  # ถ้าไม่พบไฟล์ให้กำหนด items เป็นรายการว่าง

         # เช็คเงื่อนไขว่า items เป็นรายการว่างหรือไม่
        if len(items) == 0:
            for i in range(3):
                item = {'id': i, "name": "example001", 'desc': "description", 'img': "static/image/OIP.jpg"}
                items.append(item)  # เพิ่ม item ลงใน items

                # คำสั่งเปิดไฟล์เพื่อเขียน
                with open('static/item.txt', 'wb') as h:
                # คำสั่งเก็บข้อมูลลงในไฟล์
                    pickle.dump(items, h)
                    
  #จัด Group List ให้เป็น 3item เนื่องจาก ในหน้า Index เราจัดให้แสดงผลแค่3 item ต่อ1แถว 
  #code แบบสั้น group_item = [items[i:i+3] for i in range(0,len(items),3)]
    grouped_items = []
    for i in range(0, len(items), 3):
        grouped_items.append(items[i:i+3])  
        
    #สร้างเงื่อนไขเช็ค การรับค่าform จากผู้ใช้
    #add item
    if request.method == 'POST':
        form = request.form
        img = request.files['file']
        name = form['name']
        desc = form['desc']
        
        img_path = os.path.join('static/image', img.filename) # type: ignore
        img.save(img_path)
        item = {'id': str(uuid.uuid4()), 'name': name, 'desc':desc, 'img':img_path}
        items.append(item)
        
        with open('static/item.txt', 'wb') as h:
            # คำสั่งเก็บข้อมูลลงในไฟล์
            pickle.dump(items, h)
            
            
            #จัด Group List ให้เป็น 3item เนื่องจาก ในหน้า Index เราจัดให้แสดงผลแค่3 item ต่อ1แถว 
  #code แบบสั้น group_item = [items[i:i+3] for i in range(0,len(items),3)]
    grouped_items = []
    for i in range(0, len(items), 3):
        grouped_items.append(items[i:i+3])  
        
        
    else:   
     #จัด Group List ให้เป็น 3item เนื่องจาก ในหน้า Index เราจัดให้แสดงผลแค่3 item ต่อ1แถว 
  #code แบบสั้น group_item = [items[i:i+3] for i in range(0,len(items),3)]
     grouped_items = []
    for i in range(0, len(items), 3):
        grouped_items.append(items[i:i+3])     
        
    return render_template('index.html', items=grouped_items)


#-------------------------------------------------------------------------------------------------------------------------  
#Delete หน้าitem.html
@app.route('/delete/<id>', methods=['DELETE'])  # type: ignore
#Delete หน้า index.html
@app.route('/delete', methods=['POST'])  # type: ignore
def delete(id):
    
   
    with open('static/item.txt', 'rb') as h:
        items = pickle.load(h)
    if request.method == "POST":
        selected_items = request.form.getlist('name')
        for i in selected_items:
            sel_item = eval(i)
            items.remove(sel_item)
        with open('static/item.txt', 'wb') as h:
          pickle.dump(items, h)
        return redirect(url_for('index'))
    
          #Delete หน้า Item.html
          #สร้างเงื่อนไขถ้า method ที่ได้รับมาเป็น Delete เราจะจัดการยังไง เติมelif ลงไปเพิ่ม
          
          
          
          
          
    elif request.method =='DELETE' :
        #อย่าลืมประกาศ ตัวแปร item
    
        #เช็คว่า user กด Delete Id item ตัวไหนให้ดึง id นั้นออกมา
        item_to_delete = next((item for item in items if item['id'] == id), None)

        # ถ้าเจอไอเท็มที่ต้องการลบ
    if item_to_delete:
        items.remove(item_to_delete)
        with open('static/item.txt', 'wb') as h:
          pickle.dump(items, h)
        
        return url_for('index')
#--------------------------------------------------------------------------------------------------------------------------

#สร้างหน้า item และดึงค่า ID มาแสดงผล
@app.route('/item/<id>', methods=['POST', 'GET'])
def about_item(id):
    
    # เปิด file ในการอ่านข้อมมูล
    with open('static/item.txt', 'rb') as h:
        items = pickle.load(h)
        #เงื่อนไข ถ้ามีการแก้ไข
    if request.method == 'POST':
        #รับค่า
        form = request.form
        img = request.files['file']
        name = form['name']
        desc = form['desc']
        #การวนลูป เรียกหา item เพื่อดู item ที่ต้องการแก้ไข หรืออ่านออกมา   
        item = [i for i in items if i['id'] == id][0]
        #เก็บตัวแปร ข้อมูลที่มีการแก้ไข
        item['name'] = name
        item['desc'] = desc
    
        #เงื่อนไข เช็คว่ารูปถูก แก้ไขหรือไม่  ถ้าถูกโพสจะทำการแก้ไข
        if img:
            #แก้ไข img_path
            img_path = os.path.join('static/image', img.filename)  # type: ignore
            #save ไฟล์รูปภาพ
            img.save(img_path)
            item['img'] = img_path
        #เปิดไฟล์เพื่อเก็บข้อมูล
        with open('static/item.txt', 'wb') as h:
            pickle.dump(items, h)
    else:
        #การวนลูป แสดง id item     
        item = [i for i in items if i['id'] == id][0]
    #แสดงผลหน้า Item   
    return render_template('item.html',item=item)
    
    

if __name__ =="__main__":
    app.run(debug=True)