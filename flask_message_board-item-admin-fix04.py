from flask import Flask,render_template,request,redirect,url_for,session,g,escape,Markup
from datetime import datetime
import os 
import sqlite3

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24) #加密,使用os模塊的urandom函數來獲得隨機值
        #Session, Cookies以及一些第三方擴展都會用到SECRET_KEY值，這是一個比較重要的配置值。
@app.route('/')
def index():
        #name = session.get('session_name')
        
        #if name:
                return render_template('index.html')
        #else:
               #return render_template('login.html') 
@app.route('/regist/',methods=['GET','POST']) #GET是用來故意讓使用者知道所以會顯是在網址列上,而post則是會隱藏資料,post可以傳很多資料可是get只能傳一很少
def regist():
        if request.method =='GET': 
                return render_template('regist.html')
        else:
                name = request.form.get('name')
                password1 = request.form.get('password1')
                password2 = request.form.get('password2')
                print('name',name)
                print('password1',password1)
                print('password1',password2)
                #save_regist(name,password1,password2)#進行部分核對                
                                        #用戶名被註冊過就不能在註冊
                conn = sqlite3.connect('messageregist.db')   #取出所有資料庫的name進行比較
                curs= conn.cursor()
                curs.execute("SELECT * FROM regist where name = '" + name + "'")#抓資料庫name
                A=curs.fetchall()
                print(A)
                if A:
                        print('已有相同用戶名')                        
                        return u'已有相同用戶名'
                else:
                        if password1!=password2:
                                return u'兩次密碼不相等，請重新輸入'
                        else:
                                password=password1
                                curs.execute("INSERT INTO regist VALUES('" + name + "','" + str(password) + "')")
                                #print(name)     #匯進數據庫
                                #print(password)
                                
                                conn.commit()
                                curs.close()
                                conn.close()

                                return redirect(url_for('login'))               


@app.route('/login/',methods=['GET','POST'])
def login():
        if request.method =='GET':
                return render_template('login.html')
        else:
                name = request.form.get('name')
                password = request.form.get('password')
                
                
                conn = sqlite3.connect('messageregist.db')
                curs= conn.cursor()
                curs.execute("SELECT * FROM regist where name = '" + name + "'")#抓資料庫name,然後比對
                A=curs.fetchall()
                #print(A)
                if not A:
                        print("用戶名錯誤") #用戶名與資料庫不相同
                        return u'用戶名錯誤'
                else:
                        #取密碼方法一
                        curs.execute("SELECT * FROM regist where password = '" + password + "' AND name = '" + name + "'")#抓資料庫密碼和名字
                        B=curs.fetchall()
                        print(B)

                        if not B:
                                print("密碼錯誤") #密碼與資料庫不相同
                                return u'密碼錯誤'
                        
                        #取密碼方法二
                        #curs.execute("SELECT * FROM regist where name = '" + name + "'")#抓資料庫name
                        #for row in curs.fetchall():                        
                        #        print(row)
                        #        dbpassword=row[1]
                        #        print("資料庫的密碼為:"+dbpassword)
                        #        print("輸入的密碼為:"+password)                                
                        
                        #if password!= dbpassword:
                        #        print("密碼錯誤") #密碼與資料庫不相同
                        #        return u'密碼錯誤'

                        else:
                                #print(name)
                                #print(password)             #登入成功後將用戶名存入session如此一來切換網頁都可以用session來儲存	
                                session['session_name']=name #設定session的變數值，也就是說把得到的用戶名丟進session，並且將這個session取名叫session_name
                                print("session的名字"+name)
                                if name=='admin':
                                        return redirect(url_for('admin'))#render_template('admine.html')#u'管理者頁面'#return redirect('/admin')新增approute及html
                                else:                                        
                                        return redirect(url_for('message'))
                       
                        conn.commit()
                        curs.close()
                        conn.close()

@app.route('/fixpassword',methods=['GET','POST'])
def fixpassword():
        name = session.get('session_name')        
        if name:
                if request.method =='GET':
                        return render_template('fixpassword.html')
                else:
                        oldpassword = request.form.get('oldpassword') #用戶輸入的舊密碼
                        newpassword1 = request.form.get('newpassword1')#用戶輸入的新密碼
                        newpassword2 = request.form.get('newpassword2')#用戶輸入的新密碼確認
                        print('oldpassword',oldpassword)
                        print('newpassword1',newpassword1)
                        print('newpassword2',newpassword2)
                        conn = sqlite3.connect('messageregist.db')   #取出所有資料庫的name進行比較
                        curs= conn.cursor()
                        curs.execute("SELECT * FROM regist where name = '" + name + "'")#抓資料庫name
                        for row in curs.fetchall():  #用方法二找密碼                      
                                print(row)
                                dbpassword=row[1]
                                print("資料庫的密碼為:"+dbpassword)
                                print("使用者輸入的舊密碼為:"+oldpassword) 
                        if oldpassword != dbpassword:
                                return u'舊密碼輸入錯誤'        
                        else:
                                if newpassword1!=newpassword2:
                                        return u'兩次新密碼不相等，請重新輸入'
                                else:
                                        curs.execute("UPDATE regist set password='" + newpassword1 + "'where name='" + name + "'")    
                                        conn.commit()                                            
                                        curs.close()
                                        conn.close()
                                        return redirect(url_for('message'))
        else:
                return redirect('/login') 

#登出
@app.route('/logout/')
def logout():
        session.clear()
        return redirect(url_for('login'))


@app.route('/message/')
def message():
        list= load_data()
        name = session.get('session_name')#新的變數名稱name，等於從session裡面抓上面設定的session_name的值
        login_name=name
        return render_template('message.html',list=list,login_name=login_name) #jinja {% if login_name==item.name %} 來判斷是否出顯示按鈕
@app.route('/post',methods=['POST']) #斜線(/)什麼為自己取名
def post(): #讀取所輸入的文字
        name = session.get('session_name')
        
        if name:
                
                comment=request.form.get('comment','暫無留言')    
                create_time = datetime.now()    
                save_data(name,comment,create_time)#這裡為什麼要兩次
                return redirect('/message')
        else:

                '''
                name='未登入帳戶'
                comment=request.form.get('comment','暫無留言')
                create_time = datetime.now()    
                save_data(name,comment,create_time)#這裡為什麼要兩次
                return redirect('/message')
                '''
                return redirect('/login')



def save_data(name,comment,create_time): #儲存至資料庫
        conn = sqlite3.connect('messageregist.db')
        curs= conn.cursor()
        curs.execute("INSERT INTO message VALUES(NULL,'" + name + "','" + comment + "','" + str(create_time) + "')")
        #print(name)
        #print(comment)
        #print(create_time)
    
        conn.commit()
        curs.close()
        conn.close()
    
def load_data(): #從資料庫取出放入list
        conn = sqlite3.connect('messageregist.db')
        curs= conn.cursor()
        curs.execute('SELECT * FROM message')
        listA=[]
        for row in curs.fetchall():
        
                a={}
                a['number']=row[0]
                a['name']=row[1]#將list改為字典型式,如name:row[0]的東西
                a['comment']=row[2]
                a['create_time']=row[3]
                listA.append(a)
        curs.close()
        conn.close()    
        return listA

@app.route('/delete',methods=['POST'])
def delete_data():  #刪除資料庫
        name = session.get('session_name')
        if name:
                messagenumber = request.form.get('messagenumber','NULL')   #message.html設定item.number是messagenumber             
                action = request.form.get('action','NULL')#將按鈕抓進來
                #print(messagenumber)
                if action == 'Delete': #判斷按鈕的地方
                        conn = sqlite3.connect('messageregist.db')
                        curs= conn.cursor()
                        curs.execute("DELETE from message where number='" + messagenumber + "'")
                        conn.commit()
                        return redirect('/message')
                elif action == 'Update':
                        conn = sqlite3.connect('messageregist.db')
                        curs= conn.cursor()
                        curs.execute("SELECT * FROM message where number='" + messagenumber + "'")

                        for row in curs.fetchall():        
                                b={}
                                b['number']=row[0]
                                b['name']=row[1]#將list改為字典型式,如name:row[0]的東西
                                b['comment']=row[2]
                                b['create_time']=row[3]
                                curs.close()
                                conn.close()  
                                return render_template('fix.html',listB=b)
        else:
                return redirect('/login')

@app.route('/fix',methods=['POST']) #從HTML中action="/fix"的HTML抓資料進來
def fix_data():
    messagenumber = request.form.get('messagenumber','NULL')
    print(messagenumber)
    comment=request.form.get('comment','NULL')    
    create_time = datetime.now()
    print(messagenumber)
    print(comment)
    print(create_time)
    conn = sqlite3.connect('messageregist.db')
    curs= conn.cursor()

    #UPDATE:修改資料庫
    curs.execute("UPDATE message set comment='" + comment + "',create_time='" + str(create_time) + "' where number='" + messagenumber + "'")
    conn.commit()                                                

    curs.close()
    conn.close()    
    return redirect('/message')


########################
@app.context_processor
#Flask 上下文處理器自動向模板的上下文中插入新變量。上下文處理器在模板渲染之前運行，並且可以在模板上下文中插入新值。
def my_context_processor():
        session_name = session.get('session_name')
        if session_name:
                return {'name':session_name} #返回字典
        return{}#沒有這個用戶返回空
#本段程式是如果session抓到名字的話就把name丟到前端，沒抓到的話就丟"空"給前端
#所有render_template後面+,name=name也能有同等效果
####################        

@app.template_filter('nl2br')
def nl2br_filter(s):
    return escape(s).replace('\n',Markup('<br>'))
                                                              
######

@app.route('/admin/') #要用session
def admin():#管理者頁面 能刪出修改所有留言及用戶名
        name = session.get('session_name')        
        if name:
                list= load_data()
                return render_template('admin.html',list=list)
        else:
                return redirect('/login')

@app.route('/adminmessage',methods=['GET','POST'])
def adminmessage():
        name = session.get('session_name')        
        if name:
                if request.method =='GET': 
                        return render_template('adminmessage.html')
                else:
                        #list= load_data()                
                        #login_name=name
                        admin_name='管理員'
                        comment=request.form.get('comment')    
                        create_time = datetime.now()
                        conn = sqlite3.connect('messageregist.db')
                        curs= conn.cursor()
                        curs.execute("INSERT INTO message VALUES(NULL,'" + admin_name + "','" + comment + "','" + str(create_time) + "')")
                        #print(name)
                        #print(comment)
                        #print(create_time)
    
                        conn.commit()
                        curs.close()
                        conn.close()
                        return redirect('/admin')#,list=list,login_name=login_name)
        else:
                return redirect('/login')
 

@app.route('/admindelete',methods=['POST'])
def admin_delete_data():#管理者刪除留言
        messagenumber = request.form.get('messagenumber','NULL')   #admin.html設定item.number是messagenumber             
        #action = request.form.get('action','NULL')#將按鈕抓進來        
        conn = sqlite3.connect('messageregist.db')
        curs= conn.cursor()
        curs.execute("DELETE from message where number='" + messagenumber + "'")
        conn.commit()
        return redirect('/admin')

@app.route('/adminuser/')
def adminuser():
        name = session.get('session_name')
        if name:
                list= load_regist_data()#list是很多字典         
                return render_template('adminuser.html',list=list)
        else:
                return redirect('/login')

def load_regist_data(): #從資料庫取出放入list
        conn = sqlite3.connect('messageregist.db')
        curs= conn.cursor()
        curs.execute('SELECT * FROM regist')
        listA=[]
        for row in curs.fetchall():
        
                a={}
                a['name']=row[0]
                a['password']=row[1]#將list改為字典型式,如name:row[0]的東西                
                listA.append(a)
                #print(listA)
        curs.close()
        conn.close()    
        return listA

@app.route('/adminuserdelete',methods=['POST'])
def userdelete():  #刪除資料庫
        name = session.get('session_name')
        if name:
                #
                username = request.form.get('username','NULL')   #message.html設定item.number是messagenumber
                #adminuser.html設定name 哪裡錯阿
                #print(username)  #刪錯         
                action = request.form.get('action','NULL')#將按鈕抓進來
                #print(messagenumber)
                if action == 'Delete': #判斷按鈕的地方#
                        #print("新用戶名" + username)                        
                        #return redirect('/adminuser')#測試
                        conn = sqlite3.connect('messageregist.db')
                        curs= conn.cursor()
                        curs.execute("DELETE from message where name='" + username + "'")
                        curs.execute("DELETE from regist where name='" + username + "'")
                        conn.commit()
                        return redirect('/adminuser')
                        
                elif action == 'Updateuser':
                        conn = sqlite3.connect('messageregist.db')
                        curs= conn.cursor()
                        curs.execute("SELECT * FROM regist where name='" + username + "'")

                        for row in curs.fetchall():        
                                b={}
                                b['name']=row[0]
                                b['password']=row[1]#將list改為字典型式,如name:row[0]的東西
                                print(b)                              
                                
                                curs.close()
                                conn.close()  
                                return render_template('adminfixname.html',listB=b)
                
                elif action == 'Updatepassword':
                        conn = sqlite3.connect('messageregist.db')
                        curs= conn.cursor()
                        curs.execute("SELECT * FROM regist where name='" + username + "'")

                        for row in curs.fetchall():        
                                b={}
                                b['name']=row[0]
                                b['password']=row[1]#將list改為字典型式,如name:row[0]的東西
                                print(b)                              
                                
                                curs.close()
                                conn.close()  
                                return render_template('adminfixpassword.html',listB=b)
                                
        else:
                return redirect('/login')


@app.route('/adminfixname',methods=['POST']) #從HTML中action="/fix"的HTML抓資料進來
def adminfixname():
        username = request.form.get('username')
        newname = request.form.get('newname')
        print("修改前名稱:"+username)
        print("修改後名稱:"+newname)
       
        conn = sqlite3.connect('messageregist.db')
        curs= conn.cursor()
        
        curs.execute("SELECT * FROM regist where name = '" + newname + "'")#抓資料庫name
        A=curs.fetchall()
        print(A)
        if A:
                print('已有相同用戶名')                        
                return u'已有相同用戶名'
        else:
         
                #UPDATE:修改資料庫 這裡要同時修改兩個資料庫
                curs.execute("UPDATE regist set name='" + newname + "'where name='" + username + "'")
                curs.execute("UPDATE message set name='" + newname + "'where name='" + username + "'")
                #curs.execute("UPDATE message set comment='" + comment + "',create_time='" + str(create_time) + "' where number='" + messagenumber + "'")
                conn.commit()                                              
                curs.close()
                conn.close()    
                return redirect('/adminuser')

@app.route('/adminfixpassword',methods=['POST']) #從HTML中action="/fix"的HTML抓資料進來
def adminfixpassword():
    username = request.form.get('username')
    newpassword = request.form.get('newpassword')
    print(username)
    print("新密碼"+ newpassword)
    #return redirect('/adminuser')#測試
    conn = sqlite3.connect('messageregist.db')
    curs= conn.cursor()    
    #UPDATE:修改資料庫
    curs.execute("UPDATE regist set password='" + newpassword + "'where name='" + username + "'")    
    conn.commit()                                            
    curs.close()
    conn.close()    
    return redirect('/adminuser')

@app.route('/adminregist/',methods=['GET','POST'])
def adminregist():
        name = session.get('session_name')
        if name:
                if request.method =='GET': 
                        return render_template('adminregist.html')
                else:
                        name = request.form.get('name')
                        password1 = request.form.get('password1')
                        password2 = request.form.get('password2')
                        print('name',name)
                        print('password1',password1)
                        print('password1',password2)
                        #save_regist(name,password1,password2)#進行部分核對                
                                        #用戶名被註冊過就不能在註冊
                        conn = sqlite3.connect('messageregist.db')   #取出所有資料庫的name進行比較
                        curs= conn.cursor()
                        curs.execute("SELECT * FROM regist where name = '" + name + "'")#抓資料庫name
                        A=curs.fetchall()
                        print(A)
                        if A:
                                print('已有相同用戶名')                        
                                return u'已有相同用戶名'
                        else:
                                if password1!=password2:
                                        return u'兩次密碼不相等，請重新輸入'
                                else:
                                        password=password1
                                        curs.execute("INSERT INTO regist VALUES('" + name + "','" + str(password) + "')")
                                        #print(name)     #匯進數據庫
                                        #print(password)
                                
                                        conn.commit()
                                        curs.close()
                                        conn.close()

                                        return redirect(url_for('adminuser'))
        else:
                return redirect('/login')

######

if __name__ == '__main__':
    app.run(debug =True)

