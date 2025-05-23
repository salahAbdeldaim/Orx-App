import flet as ft
from flet import *
import os
import sqlite3
import shutil

# Color constants
red = "#FA837A"
blue = "#9B8CFA"
green = "#7AFAB0"
gray = "#D9D9D9"
gray2 = "#C7C5C5"
brown = "#7A7763"
yellow = "#FFE97B"  # Bg Color
white = "#FFFFFF"

# 🎨 ألوان دارك مود عصرية


# تحديد المسار الأساسي
base_path = os.path.dirname(os.path.abspath(__file__))

# دالة للحصول على مسار قاعدة بيانات قابلة للكتابة
def get_writable_db_path(base_path):
    data_dir = os.path.join(base_path, "Orx_data")
    writable_path = os.path.join(data_dir, "Orx_data.db")
    asset_db_path = os.path.join(base_path, "assets", "Orx_data.db")
    
    os.makedirs(data_dir, exist_ok=True)
    
    if not os.path.exists(writable_path) and os.path.exists(asset_db_path):
        print(f"نسخ قاعدة البيانات من {asset_db_path} إلى {writable_path}")
        shutil.copy(asset_db_path, writable_path)
    
    return writable_path

# الاتصال بقاعدة البيانات
db_path = get_writable_db_path(base_path)
conn = sqlite3.connect(db_path, check_same_thread=False)
cursor = conn.cursor()

# إنشاء الجداول
cursor.execute(""" 
CREATE TABLE IF NOT EXISTS store (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    store_name TEXT NOT NULL UNIQUE,
    store_phone TEXT,
    store_person1_name TEXT,
    store_person1phone TEXT,
    store_person2_name TEXT,
    store_person2phone TEXT
)
""")

cursor.execute(""" 
CREATE TABLE IF NOT EXISTS items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    item_name TEXT,
    item_type TEXT,
    store_id INTEGER,
    FOREIGN KEY (store_id) REFERENCES store(id) ON DELETE CASCADE
)
""")

cursor.execute(""" 
CREATE TABLE IF NOT EXISTS customers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_name TEXT,
    customers_phone TEXT
);
""")

cursor.execute(""" 
CREATE TABLE IF NOT EXISTS customersIemOrder (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER,                     -- هذا هو المفتاح الأجنبي
    item_name TEXT,
    quantity TEXT,
    date TEXT,
    FOREIGN KEY (customer_id) REFERENCES customers(id)
);
""")

cursor.execute(""" 
CREATE TABLE IF NOT EXISTS monthlyCustomers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    m_customer_name TEXT,
    m_customers_phone TEXT
);             
""")

cursor.execute(""" 
CREATE TABLE IF NOT EXISTS mCustomersIemOrder (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    m_customer_id INTEGER,                   -- هذا هو المفتاح الأجنبي
    m_item_name TEXT,
    m_quantity TEXT,
    FOREIGN KEY (m_customer_id) REFERENCES monthlyCustomers(id)
);
""")

cursor.execute(""" 
CREATE TABLE IF NOT EXISTS settings (
    id INTEGER PRIMARY KEY,
    app_title TEXT
)
""")
# التأكد من وجود سجل افتراضي في جدول settings
cursor.execute("INSERT OR IGNORE INTO settings (id, app_title) VALUES (?, ?)", (1, "مدير المنتجات"))
conn.commit()

# مسارات الصور
facebook = os.path.join(base_path, "assets", "facebook.png")
whatsapp = os.path.join(base_path, "assets", "whatsapp.png")
linkedin = os.path.join(base_path, "assets", "linkedin.png") 
gmail = os.path.join(base_path, "assets", "gmail.png")
cart_add = os.path.join(base_path, "assets", "cart.png")
user_add = os.path.join(base_path, "assets", "new-user.png")
user_time = os.path.join(base_path, "assets", "user_time.png")
searching_icon = os.path.join(base_path, "assets", "searching.png")
add_icon = os.path.join(base_path, "assets", "add.png")
search_person_icon = os.path.join(base_path, "assets", "search_person.png")

# دوال مساعدة
def dropdown_changed(e, page):
    print(f"Selected value: {e.control.value}")
    page.update()

def create_dropdown(options, hint_text, default_value, width=301, page=None):
    return Dropdown(
        width=width,
        border_radius=24,
        hint_text=hint_text,  # النص التوضيحي عندما تكون القائمة فارغة
        options=[ft.dropdown.Option(opt) for opt in options],
        value=default_value,  # القيمة الافتراضية
        on_change=lambda e: dropdown_changed(e, page)
    )

history = []

def show_popup_page(content, page):
    if content not in history:
        history.append(content)
    content_container.content = content
    page.update()

def go_back(page, pages):
    if len(history) > 1:
        history.pop()
        previous = history[-1]
        content_container.content = previous
    elif len(history) == 1:
        content_container.content = pages[0]
        history.clear()
        history.append(pages[0])
    page.update()

def on_nav_change(e, page, pages):
    selected_index = e.control.selected_index
    print("Navigation changed to index:", selected_index)
    content_container.content = pages[selected_index]
    if pages[selected_index] not in history:
        history.append(pages[selected_index])
    page.update()
 

item_name = TextField(
    hint_text='اسم الصنف',
    height=48,
    width=301,
    border_radius=24,
    color='black',
    text_align=TextAlign.RIGHT,
    bgcolor=white,  # خلفية رمادية عادية
    border_color='gray',  # لون الإطار الطبيعي
    focused_border_color=blue  # لون الإطار عند التركيز
)


def create_home_page(store_names,page):

    
        
    btn1 = Container(
        width=310,
        height=165,
        bgcolor=gray2,
        border_radius=24,
        alignment=alignment.center,
        content=Container(
            width=300,
            height=150,
            bgcolor=gray,
            border_radius=24,
            alignment=alignment.center,
            content=TextButton(
                content=Row(
                    controls=[
                        Text("اضف صنفا!", size=18, weight=FontWeight.BOLD, color=brown),
                        Image(cart_add,width=100,height=100, color=brown),
                    ],
                    alignment="center",
                    spacing=10,
                ),
                width=300,
                height=150,
                style=ButtonStyle(bgcolor=gray, color=brown, padding=0),
                on_click=lambda e: show_popup_page(create_add_item_home_page(store_names,page),page),
            ),
        ),margin=margin.only(top=40),
    )

    btn2 = Container(
        width=310,
        height=165,
        bgcolor=gray2,
        border_radius=24,
        alignment=alignment.center,
        content= Container(
        width=300,
        height=150,
        bgcolor=gray,
        border_radius=24,
        alignment=alignment.center,
        content=TextButton(content=Row(controls=[
                        Text(" اطلب لعميل", size=18, weight=FontWeight.BOLD, color=brown),
                        Image(user_add,width=100,height=100, color=brown),],alignment="center",),
                         

                        width=300,
                        height=150,
                        style=ButtonStyle(bgcolor=gray, color=brown, padding=0,),
                        on_click=lambda e: show_popup_page(create_ordr_registration_home_page(store_names, page),page),
                  
                ),
    )) 

    btn3 = Container(
        width=310,
        height=165,
        bgcolor=gray2,
        border_radius=24,
        alignment=alignment.center,
        content= Container(
        width=300,
        height=150,
        bgcolor=gray,
        border_radius=24,
        alignment=alignment.center,
        content=TextButton(content=Row(controls=[
                        Text("فواتير شهرية!", size=18, weight=FontWeight.BOLD, color=brown),
                        Image(user_time,width=100,height=100, color=brown),],alignment="center",),
                         

                        width=300,
                        height=150,
                        style=ButtonStyle(bgcolor=gray, color=brown, padding=0,),
                        on_click=lambda e: show_popup_page(create_add_mcustomer_home_page(store_names, page),page),
                  
                ),
    ))

    page_content = Column(
        controls=[btn1,btn2,btn3],
        spacing=20,
        expand=True,
        alignment=MainAxisAlignment.CENTER,
        horizontal_alignment=CrossAxisAlignment.CENTER,
    )

    page.update()
    return page_content

# Ask_for_customer done = wait
def create_ordr_registration_home_page(store_names, page):
    
    
    head = Container(
        width=300,
        height=60,
        bgcolor=blue,
        border_radius=24,
        alignment=alignment.center,
        content=Row(
            [
                Text(
                    "الفواتير الشهرية!",
                    color=white,
                    size=24,
                    weight=FontWeight.BOLD,
                )
            ],
            alignment=MainAxisAlignment.CENTER
        ),
        margin=margin.only(top=50)
        
    )

    
    btn1 = Container(
        width=310,
        height=165,
        bgcolor=gray2,
        border_radius=24,
        alignment=alignment.center,
        content=Container(
            width=300,
            height=150,
            bgcolor=gray,
            border_radius=24,
            alignment=alignment.center,
            content=TextButton(
                content=Row(
                    controls=[
                        Text("سجل طلبية!", size=18, weight=FontWeight.BOLD, color=brown),
                        Image(add_icon,width=100,height=100, color=brown),
                    ],
                    alignment="center",
                    spacing=10,
                ),
                width=300,
                height=150,
                style=ButtonStyle(bgcolor=gray, color=brown, padding=0),
                on_click=lambda e: show_popup_page(create_ordr_registration_page(store_names, page),page),
            ),
        ),margin=margin.only(top=50),
    )

    btn2 = Container(
        width=310,
        height=165,
        bgcolor=gray2,
        border_radius=24,
        alignment=alignment.center,
        content= Container(
        width=300,
        height=150,
        bgcolor=gray,
        border_radius=24,
        alignment=alignment.center,
        content=TextButton(content=Row(controls=[
                        Text("ابحث عن طلبية!", size=18, weight=FontWeight.BOLD, color=brown),
                        Image(searching_icon,width=100,height=100, color=brown),],alignment="center",),
                         
                        width=300,
                        height=150,
                        style=ButtonStyle(bgcolor=gray, color=brown, padding=0,),
                        on_click=lambda e: show_popup_page(create_order_search_page(store_names, page),page),
                  
                ),
    ))

    page_content = Column(
        controls=[head,btn1,btn2],
        spacing=20,
        expand=True,
        alignment=MainAxisAlignment.CENTER,
        horizontal_alignment=CrossAxisAlignment.CENTER,
    )

    page.update()
    return page_content

# done
def create_add_item_home_page(store_names,page):

    
    head = Container(
        width=300,
        height=60,
        bgcolor=blue,
        border_radius=24,
        alignment=alignment.center,
        content=Row(
            [
                Text(
                    "اضافة صنف ناقص!",
                    color=white,
                    size=24,
                    weight=FontWeight.BOLD,
                )
            ],
            alignment=MainAxisAlignment.CENTER
        ),
        margin=margin.only(top=50)
        
    )

    btn1 = Container(
        width=310,
        height=165,
        bgcolor=gray2,
        border_radius=24,
        alignment=alignment.center,
        content=Container(
            width=300,
            height=150,
            bgcolor=gray,
            border_radius=24,
            alignment=alignment.center,
            content=TextButton(
                content=Row(
                    controls=[
                        Text("اضافة صنف!", size=18, weight=FontWeight.BOLD, color=brown),
                        Image(cart_add,width=100,height=100, color=brown),
                    ],
                    alignment="center",
                    spacing=10,
                ),
                width=300,
                height=150,
                style=ButtonStyle(bgcolor=gray, color=brown, padding=0),
                on_click=lambda e: show_popup_page(create_page_add_item(store_names, page),page),
            ),
        ),margin=margin.only(top=50),
    )

    btn2 = Container(
        width=310,
        height=165,
        bgcolor=gray2,
        border_radius=24,
        alignment=alignment.center,
        content= Container(
        width=300,
        height=150,
        bgcolor=gray,
        border_radius=24,
        alignment=alignment.center,
        content=TextButton(content=Row(controls=[
                        Text("عرض الاصناف المطلوبة!", size=18, weight=FontWeight.BOLD, color=brown),
                        Image(user_time,width=100,height=100, color=brown),],alignment="center",),
                         

                        width=300,
                        height=150,
                        style=ButtonStyle(bgcolor=gray, color=brown, padding=0,),
                        on_click=lambda e: show_popup_page(create_page_view_orders(store_names, page),page),
                  
                ),
    ))

    page_content = Column(
        controls=[head,btn1,btn2],
        spacing=20,
        expand=True,
        alignment=MainAxisAlignment.CENTER,
        horizontal_alignment=CrossAxisAlignment.CENTER,
    )

    page.update()
    return page_content

# add_customer_home_page done = wait
def create_add_mcustomer_home_page(store_names, page):
    
    head = Container(
        width=300,
        height=60,
        bgcolor=blue,
        border_radius=24,
        alignment=alignment.center,
        content=Row(
            [
                Text(
                    "الفواتير الشهرية!",
                    color=white,
                    size=24,
                    weight=FontWeight.BOLD,
                )
            ],
            alignment=MainAxisAlignment.CENTER
        ),
        margin=margin.only(top=50)
        
    )


    btn1 = Container(
        width=310,
        height=165,
        bgcolor=gray2,
        border_radius=24,
        alignment=alignment.center,
        content=Container(
            width=300,
            height=150,
            bgcolor=gray,
            border_radius=24,
            alignment=alignment.center,
            content=TextButton(
                content=Row(
                    controls=[
                        Text("سجل عميل", size=18, weight=FontWeight.BOLD, color=brown),
                        Image(add_icon,width=100,height=100, color=brown),
                    ],
                    alignment="center",
                    spacing=10,
                ),
                width=300,
                height=150,
                style=ButtonStyle(bgcolor=gray, color=brown, padding=0),
                on_click=lambda e: show_popup_page(create_mcustomer_add_page(store_names, page),page),
            ),
        ),margin=margin.only(top=50),
    )

    btn2 = Container(
        width=310,
        height=165,
        bgcolor=gray2,
        border_radius=24,
        alignment=alignment.center,
        content= Container(
        width=300,
        height=150,
        bgcolor=gray,
        border_radius=24,
        alignment=alignment.center,
        content=TextButton(content=Row(controls=[
                        Text("ابحث عن عميل!", size=18, weight=FontWeight.BOLD, color=brown),
                        Image(search_person_icon,width=100,height=100, color=brown),],alignment="center",),
                         

                        width=300,
                        height=150,
                        style=ButtonStyle(bgcolor=gray, color=brown, padding=0,),
                        on_click=lambda e: show_popup_page(create_mcustomer_serch_page(store_names, page),page),
                  
                ),
    ))

    page_content = Column(
        controls=[head,btn1,btn2],
        spacing=20,
        expand=True,
        alignment=MainAxisAlignment.CENTER,
        horizontal_alignment=CrossAxisAlignment.CENTER,
    )

    page.update()
    return page_content



person_name_ask   = TextField(hint_text='اسم العميل'       , height=48,width=301,border_radius=24,color='black',bgcolor=white,border_color='gray',focused_border_color=blue,text_align=TextAlign.RIGHT,)
person_phone_ask  = TextField(hint_text='رقم هاتف العميل'  , height=48,width=301,border_radius=24,color='black',bgcolor=white,border_color='gray',focused_border_color=blue,text_align=TextAlign.RIGHT,)
date_input_ask   = TextField(hint_text='التاريخ' , height=48,width=301,border_radius=24,color='black',bgcolor=white,border_color='gray',focused_border_color=blue,text_align=TextAlign.RIGHT,)
item_type_ask  = TextField(hint_text='اسم الصنف', height=48,width=301,border_radius=24,color='black',bgcolor=white,border_color='gray',focused_border_color=blue,text_align=TextAlign.RIGHT,)

#win_Ask_for_customer done

def create_ordr_registration_page(store_names, page):
    # قائمة أيام الأسبوع
    days_of_week = ["السبت", "الأحد", "الإثنين", "الثلاثاء", "الأربعاء", "الخميس", "الجمعة"]
    date_dropdown = create_dropdown(
        options=days_of_week,
        hint_text="اختر اليوم",
        default_value=days_of_week[0],
        page=page
    )

    def add_order(e, page):
        customer_name = person_name_ask.value.strip()
        customer_phone = person_phone_ask.value.strip()
        order_date = date_dropdown.value
        item_name = item_type_ask.value.strip()
        quantity = "1"

        if not all([customer_name, customer_phone, order_date, item_name]):
            alert_dialog = ft.AlertDialog(
                title=ft.Text("خطأ"),
                content=ft.Text("يرجى ملء كل الحقول"),
                actions=[
                ],
                actions_alignment=ft.MainAxisAlignment.END,
                bgcolor=red
            )
            page.overlay.append(alert_dialog)
            alert_dialog.open = True
            page.update()
            return

        try:
            cursor.execute("SELECT id FROM customers WHERE customer_name = ? AND customers_phone = ?",
                           (customer_name, customer_phone))
            result = cursor.fetchone()
            if not result:
                cursor.execute("INSERT INTO customers (customer_name, customers_phone) VALUES (?, ?)",
                               (customer_name, customer_phone))
                conn.commit()
                cursor.execute("SELECT id FROM customers WHERE customer_name = ? AND customers_phone = ?",
                               (customer_name, customer_phone))
                result = cursor.fetchone()

            customer_id = result[0]
            cursor.execute("INSERT INTO customersIemOrder (customer_id, item_name, quantity, date) VALUES (?, ?, ?, ?)",
                           (customer_id, item_name, quantity, order_date))
            conn.commit()

            alert_dialog = ft.AlertDialog(
                title=ft.Text("نجاح"),
                content=ft.Text("تم تسجيل الطلب بنجاح"),
                actions=[
                ],
                actions_alignment=ft.MainAxisAlignment.END,
                bgcolor=green
            )
            page.overlay.append(alert_dialog)
            alert_dialog.open = True
            person_name_ask.value = ""
            person_phone_ask.value = ""
            date_dropdown.value = days_of_week[0]
            item_type_ask.value = ""

        except sqlite3.Error as err:
            alert_dialog = ft.AlertDialog(
                title=ft.Text("خطأ"),
                content=ft.Text(f"خطأ في قاعدة البيانات: {err}"),
                actions=[
                ],
                actions_alignment=ft.MainAxisAlignment.END,
                bgcolor=red
            )
            page.overlay.append(alert_dialog)
            alert_dialog.open = True

        page.update()

    def delete_order(e, page):
        customer_name = person_name_ask.value.strip()
        item_name = item_type_ask.value.strip()

        if not all([customer_name, item_name]):
            alert_dialog = ft.AlertDialog(
                title=ft.Text("خطأ"),
                content=ft.Text("يرجى إدخال اسم العميل واسم الصنف للحذف"),
                actions=[
                ],
                actions_alignment=ft.MainAxisAlignment.END,
                bgcolor=red
            )
            page.overlay.append(alert_dialog)
            alert_dialog.open = True
            page.update()
            return

        try:
            cursor.execute("SELECT id FROM customers WHERE customer_name = ?", (customer_name,))
            result = cursor.fetchone()
            if not result:
                alert_dialog = ft.AlertDialog(
                    title=ft.Text("خطأ"),
                    content=ft.Text("لم يتم العثور على العميل"),
                    actions=[
                    ],
                    actions_alignment=ft.MainAxisAlignment.END,
                    bgcolor=red
                )
                page.overlay.append(alert_dialog)
                alert_dialog.open = True
                page.update()
                return

            customer_id = result[0]
            cursor.execute(
                "DELETE FROM customersIemOrder WHERE customer_id = ? AND item_name = ?",
                (customer_id, item_name)
            )
            if cursor.rowcount == 0:
                alert_dialog = ft.AlertDialog(
                    title=ft.Text("خطأ"),
                    content=ft.Text("لم يتم العثور على الطلب للحذف"),
                    actions=[
                    ],
                    actions_alignment=ft.MainAxisAlignment.END,
                    bgcolor=red
                )
            else:
                conn.commit()
                alert_dialog = ft.AlertDialog(
                    title=ft.Text("نجاح"),
                    content=ft.Text("تم حذف الطلب بنجاح"),
                    actions=[
                    ],
                    actions_alignment=ft.MainAxisAlignment.END,
                    bgcolor=green
                )
                person_name_ask.value = ""
                person_phone_ask.value = ""
                date_dropdown.value = days_of_week[0]
                item_type_ask.value = ""

            page.overlay.append(alert_dialog)
            alert_dialog.open = True
            page.update()

        except sqlite3.Error as err:
            alert_dialog = ft.AlertDialog(
                title=ft.Text("خطأ"),
                content=ft.Text(f"خطأ في قاعدة البيانات: {err}"),
                actions=[
                ],
                actions_alignment=ft.MainAxisAlignment.END,
                bgcolor=red
            )
            page.overlay.append(alert_dialog)
            alert_dialog.open = True
            page.update()

    main_rect = Container(
        expand=True,
        width=345,
        height=400,
        bgcolor=gray,
        border_radius=24,
        alignment=alignment.center,
        margin=margin.only(top=100),
        content=Column(
            controls=[
                Container(
                    width=301,
                    bgcolor=white,
                    border_radius=24,
                    alignment=alignment.center,
                    content=person_name_ask
                ),
                Container(
                    width=301,
                    bgcolor=white,
                    border_radius=24,
                    alignment=alignment.center,
                    content=person_phone_ask
                ),
                Container(
                    width=301,
                    bgcolor=white,
                    border_radius=24,
                    alignment=alignment.center,
                    content=date_dropdown
                ),
                Container(
                    width=301,
                    bgcolor=white,
                    border_radius=24,
                    alignment=alignment.center,
                    content=item_type_ask
                ),
            ],
            spacing=15,
            alignment=MainAxisAlignment.CENTER,
        )
    )

    sec_rect = Container(
        width=300,
        height=60,
        bgcolor=blue,
        border_radius=24,
        alignment=alignment.center,
        margin=margin.only(top=50),
        content=Row(
            [
                Text(
                    "طلب منتج لعميل!",
                    color=white,
                    size=24,
                    weight=FontWeight.BOLD,
                )
            ],
            alignment=MainAxisAlignment.CENTER
        )
    )

    b1 = ElevatedButton(
        content=Text("اضافة", size=18, weight=FontWeight.BOLD),
        width=150,
        style=ButtonStyle(bgcolor=blue, color=white, padding=15),
        on_click=lambda e: add_order(e, page),
    )

    b2 = ElevatedButton(
        content=Text("حذف", size=18, weight=FontWeight.BOLD),
        width=150,
        style=ButtonStyle(bgcolor=blue, color=white, padding=15),
        on_click=lambda e: delete_order(e, page),
    )

    page_content = Column(
        controls=[
            Stack(controls=[main_rect, Container(content=sec_rect, margin=margin.only(top=-30))], alignment=alignment.top_center),
            Row([b1, b2], alignment=MainAxisAlignment.CENTER),
        ],
        spacing=30,
        expand=True,
        alignment=MainAxisAlignment.CENTER,
        horizontal_alignment=CrossAxisAlignment.CENTER,
    )
    return page_content
 

def create_order_search_page(store_names, page):
    cursor.execute("SELECT customer_name FROM customers")
    customer_names = [row[0] for row in cursor.fetchall()]
    customer_names.insert(0, "اختر العميل")

    customer_dropdown = create_dropdown(
        options=customer_names,
        hint_text="اختر العميل",
        default_value="اختر العميل",
        page=page
    )

    cards_column = ft.Column(scroll=ft.ScrollMode.AUTO, spacing=10)

    def show_orders(e):
        selected_customer = customer_dropdown.value
        cards_column.controls.clear()

        if selected_customer == "اختر العميل":
            alert_dialog = ft.AlertDialog(
                title=ft.Text("خطأ"),
                content=ft.Text("يرجى اختيار عميل"),
                actions=[
                ],
                actions_alignment=ft.MainAxisAlignment.END,
                bgcolor=red
            )
            page.overlay.append(alert_dialog)
            alert_dialog.open = True
            page.update()
            return

        try:
            cursor.execute("SELECT id, customers_phone FROM customers WHERE customer_name = ?", (selected_customer,))
            result = cursor.fetchone()
            if not result:
                alert_dialog = ft.AlertDialog(
                    title=ft.Text("خطأ"),
                    content=ft.Text("لم يتم العثور على العميل"),
                    actions=[
                    ],
                    actions_alignment=ft.MainAxisAlignment.END,
                    bgcolor=red
                )
                page.overlay.append(alert_dialog)
                alert_dialog.open = True
                page.update()
                return

            customer_id, customer_phone = result
            cursor.execute(
                "SELECT item_name, quantity, date FROM customersIemOrder WHERE customer_id = ?",
                (customer_id,)
            )
            orders = cursor.fetchall()

            if not orders:
                cards_column.controls.append(
                    ft.Text("لا توجد طلبات لهذا العميل", size=18, color="red", text_align=ft.TextAlign.CENTER)
                )
            else:
                for item_name, quantity, order_date in orders:
                    def delete_order(e, item_name=item_name, customer_id=customer_id):
                        def confirm_delete(e):
                            try:
                                cursor.execute(
                                    "DELETE FROM customersIemOrder WHERE customer_id = ? AND item_name = ?",
                                    (customer_id, item_name)
                                )
                                if cursor.rowcount == 0:
                                    alert_dialog = ft.AlertDialog(
                                        title=ft.Text("خطأ"),
                                        content=ft.Text(f"لم يتم العثور على الطلب '{item_name}'"),
                                        actions=[
                                        ],
                                        actions_alignment=ft.MainAxisAlignment.END,
                                        bgcolor=red
                                    )
                                else:
                                    conn.commit()
                                    alert_dialog = ft.AlertDialog(
                                        title=ft.Text("نجاح"),
                                        content=ft.Text(f"تم حذف الطلب '{item_name}' بنجاح"),
                                        actions=[
                                        ],
                                        actions_alignment=ft.MainAxisAlignment.END,
                                        bgcolor=green
                                    )
                                    show_orders(None)
                                page.overlay.append(alert_dialog)
                                alert_dialog.open = True
                            except sqlite3.Error as err:
                                alert_dialog = ft.AlertDialog(
                                    title=ft.Text("خطأ"),
                                    content=ft.Text(f"خطأ في قاعدة البيانات: {err}"),
                                    actions=[
                                    ],
                                    actions_alignment=ft.MainAxisAlignment.END,
                                    bgcolor=red
                                )
                                page.overlay.append(alert_dialog)
                                alert_dialog.open = True
                            page.update()

                        def cancel_delete(e):
                            page.overlay.pop() if page.overlay else None
                            page.update()

                        alert_dialog = ft.AlertDialog(
                            title=ft.Text("تأكيد الحذف"),
                            content=ft.Text(f"هل أنت متأكد أنك تريد حذف الطلب '{item_name}'؟"),
                            actions=[
                                ft.TextButton("نعم", on_click=confirm_delete),
                                ft.TextButton("لا", on_click=cancel_delete),
                            ],
                            actions_alignment=ft.MainAxisAlignment.END,
                        )
                        page.overlay.append(alert_dialog)
                        alert_dialog.open = True
                        page.update()

                    def call_phone(e, phone=customer_phone):
                        try:
                            phone_url = f"tel:{customer_phone}"
                            page.launch_url(phone_url)
                        except Exception as err:
                            alert_dialog = ft.AlertDialog(
                                title=ft.Text("خطأ"),
                                content=ft.Text("خاصية الاتصال مدعومة فقط على الهواتف"),
                                actions=[
                                ],
                                actions_alignment=ft.MainAxisAlignment.END,
                                bgcolor=red
                            )
                            page.overlay.append(alert_dialog)
                            alert_dialog.open = True
                        page.update()

                    order_card = ft.Container(
                        content=ft.Card(
                            content=ft.Container(
                                content=ft.Row(
                                    controls=[
                                        ft.Column(
                                            controls=[
                                                ft.Text(f"الصنف: {item_name}", size=16, weight=ft.FontWeight.BOLD, color="black"),
                                                ft.Text(f"الكمية: {quantity}", size=14, color="black"),
                                                ft.Text(f"اليوم: {order_date}", size=14, color="black"),
                                                ft.GestureDetector(
                                                    on_tap=lambda e: call_phone(e, customer_phone),
                                                    content=ft.Text(
                                                        f"📞 رقم الهاتف: {customer_phone}",
                                                        size=16,
                                                        color=blue,  # اللون الأزرق #7F7AFA
                                                        weight=ft.FontWeight.BOLD
                                                    )
                                                ),
                                            ],
                                            spacing=5,
                                        ),
                                        ft.IconButton(
                                            icon=ft.Icons.DELETE,
                                            icon_color=red,
                                            tooltip="حذف الطلب",
                                            on_click=delete_order,
                                        ),
                                    ],
                                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                ),
                                padding=10,
                                bgcolor=green,
                            ),
                            elevation=2,
                            color="white",
                        ),
                        border_radius=24,
                        margin=ft.margin.only(left=5, right=5, top=5, bottom=5),
                        bgcolor="white",
                    )
                    cards_column.controls.append(order_card)

        except sqlite3.Error as err:
            alert_dialog = ft.AlertDialog(
                title=ft.Text("خطأ"),
                content=ft.Text(f"خطأ في قاعدة البيانات: {err}"),
                actions=[
                ],
                actions_alignment=ft.MainAxisAlignment.END,
                bgcolor=red
            )
            page.overlay.append(alert_dialog)
            alert_dialog.open = True

        page.update()

    def delete_all_orders(e):
        selected_customer = customer_dropdown.value

        if selected_customer == "اختر العميل":
            alert_dialog = ft.AlertDialog(
                title=ft.Text("خطأ"),
                content=ft.Text("يرجى اختيار عميل"),
                actions=[
                ],
                actions_alignment=ft.MainAxisAlignment.END,
                bgcolor=red
            )
            page.overlay.append(alert_dialog)
            alert_dialog.open = True
            page.update()
            return

        try:
            cursor.execute("SELECT id FROM customers WHERE customer_name = ?", (selected_customer,))
            result = cursor.fetchone()
            if not result:
                alert_dialog = ft.AlertDialog(
                    title=ft.Text("خطأ"),
                    content=ft.Text("لم يتم العثور على العميل"),
                    actions=[
                    ],
                    actions_alignment=ft.MainAxisAlignment.END,
                    bgcolor=red
                )
                page.overlay.append(alert_dialog)
                alert_dialog.open = True
                page.update()
                return

            customer_id = result[0]
            cursor.execute("DELETE FROM customersIemOrder WHERE customer_id = ?", (customer_id,))
            conn.commit()
            cards_column.controls.clear()
            alert_dialog = ft.AlertDialog(
                title=ft.Text("نجاح"),
                content=ft.Text("تم حذف جميع طلبات العميل"),
                actions=[
                ],
                actions_alignment=ft.MainAxisAlignment.END,
                bgcolor=green
            )
            page.overlay.append(alert_dialog)
            alert_dialog.open = True
            page.update()

        except sqlite3.Error as err:
            alert_dialog = ft.AlertDialog(
                title=ft.Text("خطأ"),
                content=ft.Text(f"خطأ في قاعدة البيانات: {err}"),
                actions=[
                ],
                actions_alignment=ft.MainAxisAlignment.END,
                bgcolor=red
            )
            page.overlay.append(alert_dialog)
            alert_dialog.open = True
            page.update()

    main_rect = Container(
        expand=True,
        width=345,
        height=150,
        bgcolor=gray,
        border_radius=24,
        alignment=alignment.center,
        margin=margin.only(top=100),
        content=Column(
            controls=[
                Container(
                    width=301,
                    bgcolor=white,
                    border_radius=24,
                    alignment=alignment.center,
                    content=customer_dropdown
                ),
            ],
            spacing=50,
            alignment=MainAxisAlignment.CENTER,
        )
    )

    sec_rect = Container(
        width=300,
        height=60,
        bgcolor=blue,
        border_radius=24,
        alignment=alignment.center,
        margin=margin.only(top=50),
        content=Row(
            [
                Text(
                    "البحث عن طلب",
                    color=white,
                    size=24,
                    weight=FontWeight.BOLD,
                )
            ],
            alignment=MainAxisAlignment.CENTER
        )
    )

    b1 = ElevatedButton(
        content=Text("عرض", size=18, weight=FontWeight.BOLD),
        width=150,
        style=ButtonStyle(bgcolor=blue, color=white, padding=15),
        on_click=lambda e: show_orders(e),
    )

    b2 = ElevatedButton(
        content=Text("حذف الكل", size=18, weight=FontWeight.BOLD),
        width=150,
        style=ButtonStyle(bgcolor=blue, color=white, padding=15),
        on_click=lambda e: delete_all_orders(e),
    )

    page_content = Column(
        controls=[
            Stack(controls=[main_rect, Container(content=sec_rect, margin=margin.only(top=-30))], alignment=alignment.top_center),
            Row([b1, b2], alignment=MainAxisAlignment.CENTER),
            Container(
                content=cards_column,
                height=300,
                width=345,
                bgcolor="#F0F0F0",
                border_radius=24,
                padding=10,
                margin=margin.only(top=20)
            )
        ],
        spacing=20,
        expand=True,
        alignment=MainAxisAlignment.CENTER,
        horizontal_alignment=CrossAxisAlignment.CENTER,
    )
    return page_content


person_name_m   = TextField(hint_text='اسم العميل'       , height=48,width=301,border_radius=24,color='black',bgcolor=white,border_color='gray',focused_border_color=blue,text_align=TextAlign.RIGHT,)
person_phone_m  = TextField(hint_text='رقم هاتف العميل'  , height=48,width=301,border_radius=24,color='black',bgcolor=white,border_color='gray',focused_border_color=blue,text_align=TextAlign.RIGHT,)
date_input_m   = TextField(hint_text='التاريخ' , height=48,width=301,border_radius=24,color='black',bgcolor=white,border_color='gray',focused_border_color=blue,text_align=TextAlign.RIGHT,)
item_type_m  = TextField(hint_text='اسم الصنف', height=48,width=301,border_radius=24,color='black',bgcolor=white,border_color='gray',focused_border_color=blue,text_align=TextAlign.RIGHT,)


def create_mcustomer_add_page(store_names, page):

    def add_mcustomer(e, page):
        customer_name = person_name_m.value.strip()
        customer_phone = person_phone_m.value.strip()
        item_name = item_type_m.value.strip()
        quantity = "1"

        if not all([customer_name, customer_phone, item_name]):
            alert_dialog = ft.AlertDialog(
                title=ft.Text("خطأ"),
                content=ft.Text("يرجى ملء كل الحقول"),
                actions=[
                ],
                actions_alignment=ft.MainAxisAlignment.END,
                bgcolor=red
            )
            page.overlay.append(alert_dialog)
            alert_dialog.open = True
            page.update()
            return

        try:
            # التحقق من وجود العميل بناءً على الاسم ورقم الهاتف
            cursor.execute(
                "SELECT id FROM monthlyCustomers WHERE m_customer_name = ? AND m_customers_phone = ?",
                (customer_name, customer_phone)
            )
            result = cursor.fetchone()

            if not result:
                # إذا لم يكن العميل موجودًا، أنشئ سجلًا جديدًا
                cursor.execute(
                    "INSERT INTO monthlyCustomers (m_customer_name, m_customers_phone) VALUES (?, ?)",
                    (customer_name, customer_phone)
                )
                conn.commit()
                cursor.execute(
                    "SELECT id FROM monthlyCustomers WHERE m_customer_name = ? AND m_customers_phone = ?",
                    (customer_name, customer_phone)
                )
                result = cursor.fetchone()

            customer_id = result[0]

            # التحقق مما إذا كان الصنف موجودًا بالفعل لنفس العميل
            cursor.execute(
                "SELECT id FROM mCustomersIemOrder WHERE m_customer_id = ? AND m_item_name = ?",
                (customer_id, item_name)
            )
            item_exists = cursor.fetchone()

            if item_exists:
                alert_dialog = ft.AlertDialog(
                    title=ft.Text("خطأ"),
                    content=ft.Text(f"الصنف '{item_name}' موجود بالفعل لهذا العميل"),
                    actions=[
                    ],
                    actions_alignment=ft.MainAxisAlignment.END,
                    bgcolor=red
                )
                page.overlay.append(alert_dialog)
                alert_dialog.open = True
                page.update()
                return

            # إضافة الصنف الجديد إلى الفاتورة
            cursor.execute(
                "INSERT INTO mCustomersIemOrder (m_customer_id, m_item_name, m_quantity) VALUES (?, ?, ?)",
                (customer_id, item_name, quantity)
            )
            conn.commit()

            alert_dialog = ft.AlertDialog(
                title=ft.Text("نجاح"),
                content=ft.Text("تم إضافة الصنف إلى الفاتورة الشهرية بنجاح"),
                actions=[
                ],
                actions_alignment=ft.MainAxisAlignment.END,
                bgcolor=green
            )
            page.overlay.append(alert_dialog)
            alert_dialog.open = True
            item_type_m.value = ""  # مسح حقل الصنف فقط

        except sqlite3.Error as err:
            alert_dialog = ft.AlertDialog(
                title=ft.Text("خطأ"),
                content=ft.Text(f"خطأ في قاعدة البيانات: {err}"),
                actions=[
                ],
                actions_alignment=ft.MainAxisAlignment.END,
                bgcolor=red
            )
            page.overlay.append(alert_dialog)
            alert_dialog.open = True

        page.update()

    def delete_mcustomer(e, page):
        customer_name = person_name_m.value.strip()
        item_name = item_type_m.value.strip()

        if not all([customer_name, item_name]):
            alert_dialog = ft.AlertDialog(
                title=ft.Text("خطأ"),
                content=ft.Text("يرجى إدخال اسم العميل واسم الصنف للحذف"),
                actions=[
                ],
                actions_alignment=ft.MainAxisAlignment.END,
                bgcolor=red
            )
            page.overlay.append(alert_dialog)
            alert_dialog.open = True
            page.update()
            return

        try:
            cursor.execute("SELECT id FROM monthlyCustomers WHERE m_customer_name = ?", (customer_name,))
            result = cursor.fetchone()
            if not result:
                alert_dialog = ft.AlertDialog(
                    title=ft.Text("خطأ"),
                    content=ft.Text("لم يتم العثور على العميل"),
                    actions=[
                    ],
                    actions_alignment=ft.MainAxisAlignment.END,
                    bgcolor=red
                )
                page.overlay.append(alert_dialog)
                alert_dialog.open = True
                page.update()
                return

            customer_id = result[0]
            cursor.execute(
                "DELETE FROM mCustomersIemOrder WHERE m_customer_id = ? AND m_item_name = ?",
                (customer_id, item_name)
            )
            if cursor.rowcount == 0:
                alert_dialog = ft.AlertDialog(
                    title=ft.Text("خطأ"),
                    content=ft.Text("لم يتم العثور على الفاتورة للحذف"),
                    actions=[
                    ],
                    actions_alignment=ft.MainAxisAlignment.END,
                    bgcolor=red
                )
            else:
                conn.commit()
                alert_dialog = ft.AlertDialog(
                    title=ft.Text("نجاح"),
                    content=ft.Text("تم حذف الفاتورة بنجاح"),
                    actions=[
                    ],
                    actions_alignment=ft.MainAxisAlignment.END,
                    bgcolor=green
                )
                item_type_m.value = ""  # مسح حقل الصنف فقط

            page.overlay.append(alert_dialog)
            alert_dialog.open = True
            page.update()

        except sqlite3.Error as err:
            alert_dialog = ft.AlertDialog(
                title=ft.Text("خطأ"),
                content=ft.Text(f"خطأ في قاعدة البيانات: {err}"),
                actions=[
                ],
                actions_alignment=ft.MainAxisAlignment.END,
                bgcolor=red
            )
            page.overlay.append(alert_dialog)
            alert_dialog.open = True
            page.update()

    main_rect = Container(
        expand=True,
        width=345,
        height=300,
        bgcolor=gray,
        border_radius=24,
        alignment=alignment.center,
        margin=margin.only(top=100),
        content=Column(
            controls=[
                Container(
                    width=301,
                    bgcolor=white,
                    border_radius=24,
                    alignment=alignment.center,
                    content=person_name_m
                ),
                Container(
                    width=301,
                    bgcolor=white,
                    border_radius=24,
                    alignment=alignment.center,
                    content=person_phone_m
                ),
                Container(
                    width=301,
                    bgcolor=white,
                    border_radius=24,
                    alignment=alignment.center,
                    content=item_type_m
                ),
            ],
            spacing=15,
            alignment=MainAxisAlignment.CENTER,
        )
    )

    sec_rect = Container(
        width=300,
        height=60,
        bgcolor=blue,
        border_radius=24,
        alignment=alignment.center,
        margin=margin.only(top=50),
        content=Row(
            [
                Text(
                    "اضف فاتورة شهرية!",
                    color=white,
                    size=24,
                    weight=FontWeight.BOLD,
                )
            ],
            alignment=MainAxisAlignment.CENTER
        )
    )

    b1 = ElevatedButton(
        content=Text("اضافة", size=18, weight=FontWeight.BOLD),
        width=150,
        style=ButtonStyle(bgcolor=blue, color=white, padding=15),
        on_click=lambda e: add_mcustomer(e, page),
    )

    b2 = ElevatedButton(
        content=Text("حذف", size=18, weight=FontWeight.BOLD),
        width=150,
        style=ButtonStyle(bgcolor=blue, color=white, padding=15),
        on_click=lambda e: delete_mcustomer(e, page),
    )

    page_content = Column(
        controls=[
            Stack(controls=[main_rect, Container(content=sec_rect, margin=margin.only(top=-30))], alignment=alignment.top_center),
            Row([b1, b2], alignment=MainAxisAlignment.CENTER),
        ],
        spacing=30,
        expand=True,
        alignment=MainAxisAlignment.CENTER,
        horizontal_alignment=CrossAxisAlignment.CENTER,
    )
    return page_content


def create_mcustomer_serch_page(store_names, page):
    cursor.execute("SELECT m_customer_name FROM monthlyCustomers")
    customer_names = [row[0] for row in cursor.fetchall()]
    customer_names.insert(0, "اختر العميل")

    customer_dropdown = create_dropdown(
        options=customer_names,
        hint_text="اختر العميل",
        default_value="اختر العميل",
        page=page
    )

    cards_column = ft.Column(scroll=ft.ScrollMode.AUTO, spacing=10)

    def show_invoices(e):
        selected_customer = customer_dropdown.value
        cards_column.controls.clear()

        if selected_customer == "اختر العميل":
            alert_dialog = ft.AlertDialog(
                title=ft.Text("خطأ"),
                content=ft.Text("يرجى اختيار عميل"),
                actions=[
                ],
                actions_alignment=ft.MainAxisAlignment.END,
                bgcolor=red
            )
            page.overlay.append(alert_dialog)
            alert_dialog.open = True
            page.update()
            return

        try:
            cursor.execute("SELECT id FROM monthlyCustomers WHERE m_customer_name = ?", (selected_customer,))
            result = cursor.fetchone()
            if not result:
                alert_dialog = ft.AlertDialog(
                    title=ft.Text("خطأ"),
                    content=ft.Text("لم يتم العثور على العميل"),
                    actions=[
                    ],
                    actions_alignment=ft.MainAxisAlignment.END,
                    bgcolor=red
                )
                page.overlay.append(alert_dialog)
                alert_dialog.open = True
                page.update()
                return

            customer_id = result[0]
            cursor.execute(
                "SELECT m_item_name, m_quantity FROM mCustomersIemOrder WHERE m_customer_id = ?",
                (customer_id,)
            )
            invoices = cursor.fetchall()

            if not invoices:
                cards_column.controls.append(
                    ft.Text("لا توجد فواتير لهذا العميل", size=18, color="red", text_align=ft.TextAlign.CENTER)
                )
            else:
                for item_name, quantity in invoices:
                    def delete_invoice(e, item_name=item_name, customer_id=customer_id):
                        def confirm_delete(e):
                            try:
                                cursor.execute(
                                    "DELETE FROM mCustomersIemOrder WHERE m_customer_id = ? AND m_item_name = ?",
                                    (customer_id, item_name)
                                )
                                if cursor.rowcount == 0:
                                    alert_dialog = ft.AlertDialog(
                                        title=ft.Text("خطأ"),
                                        content=ft.Text(f"لم يتم العثور على الفاتورة '{item_name}'"),
                                        actions=[
                                        ],
                                        actions_alignment=ft.MainAxisAlignment.END,
                                        bgcolor=red
                                    )
                                else:
                                    conn.commit()
                                    alert_dialog = ft.AlertDialog(
                                        title=ft.Text("نجاح"),
                                        content=ft.Text(f"تم حذف الفاتورة '{item_name}' بنجاح"),
                                        actions=[
                                        ],
                                        actions_alignment=ft.MainAxisAlignment.END,
                                        bgcolor=green
                                    )
                                    show_invoices(None)
                                page.overlay.append(alert_dialog)
                                alert_dialog.open = True
                            except sqlite3.Error as err:
                                alert_dialog = ft.AlertDialog(
                                    title=ft.Text("خطأ"),
                                    content=ft.Text(f"خطأ في قاعدة البيانات: {err}"),
                                    actions=[
                                    ],
                                    actions_alignment=ft.MainAxisAlignment.END,
                                    bgcolor=red
                                )
                                page.overlay.append(alert_dialog)
                                alert_dialog.open = True
                            page.update()

                        def cancel_delete(e):
                            page.overlay.pop() if page.overlay else None
                            page.update()

                        alert_dialog = ft.AlertDialog(
                            title=ft.Text("تأكيد الحذف"),
                            content=ft.Text(f"هل أنت متأكد أنك تريد حذف الفاتورة '{item_name}'؟"),
                            actions=[
                                ft.TextButton("نعم", on_click=confirm_delete),
                                ft.TextButton("لا", on_click=cancel_delete),
                            ],
                            actions_alignment=ft.MainAxisAlignment.END,
                        )
                        page.overlay.append(alert_dialog)
                        alert_dialog.open = True
                        page.update()

                    invoice_card = ft.Container(
                        content=ft.Card(
                            content=ft.Container(
                                content=ft.Row(
                                    controls=[
                                        ft.Column(
                                            controls=[
                                                ft.Text(f"الصنف: {item_name}", size=16, weight=ft.FontWeight.BOLD, color="black"),
                                                ft.Text(f"الكمية: {quantity}", size=14, color="black"),
                                            ],
                                            spacing=5,
                                        ),
                                        ft.IconButton(
                                            icon=ft.Icons.DELETE,
                                            icon_color=red,
                                            tooltip="حذف الفاتورة",
                                            on_click=delete_invoice,
                                        ),
                                    ],
                                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                ),
                                padding=10,
                                bgcolor=green,
                            ),
                            elevation=2,
                            color="white",
                        ),
                        border_radius=24,
                        margin=ft.margin.only(left=5, right=5, top=5, bottom=5),
                        bgcolor="white",
                    )
                    cards_column.controls.append(invoice_card)

        except sqlite3.Error as err:
            alert_dialog = ft.AlertDialog(
                title=ft.Text("خطأ"),
                content=ft.Text(f"خطأ في قاعدة البيانات: {err}"),
                actions=[
                ],
                actions_alignment=ft.MainAxisAlignment.END,
                bgcolor=red
            )
            page.overlay.append(alert_dialog)
            alert_dialog.open = True

        page.update()

    def delete_all_invoices(e):
        selected_customer = customer_dropdown.value

        if selected_customer == "اختر العميل":
            alert_dialog = ft.AlertDialog(
                title=ft.Text("خطأ"),
                content=ft.Text("يرجى اختيار عميل"),
                actions=[
                ],
                actions_alignment=ft.MainAxisAlignment.END,
                bgcolor=red
            )
            page.overlay.append(alert_dialog)
            alert_dialog.open = True
            page.update()
            return

        try:
            cursor.execute("SELECT id FROM monthlyCustomers WHERE m_customer_name = ?", (selected_customer,))
            result = cursor.fetchone()
            if not result:
                alert_dialog = ft.AlertDialog(
                    title=ft.Text("خطأ"),
                    content=ft.Text("لم يتم العثور على العميل"),
                    actions=[
                    ],
                    actions_alignment=ft.MainAxisAlignment.END,
                    bgcolor=red
                )
                page.overlay.append(alert_dialog)
                alert_dialog.open = True
                page.update()
                return

            customer_id = result[0]
            cursor.execute("DELETE FROM mCustomersIemOrder WHERE m_customer_id = ?", (customer_id,))
            conn.commit()
            cards_column.controls.clear()
            alert_dialog = ft.AlertDialog(
                title=ft.Text("نجاح"),
                content=ft.Text("تم حذف جميع الفواتير الشهرية للعميل"),
                actions=[
                ],
                actions_alignment=ft.MainAxisAlignment.END,
                bgcolor=green
            )
            page.overlay.append(alert_dialog)
            alert_dialog.open = True
            page.update()

        except sqlite3.Error as err:
            alert_dialog = ft.AlertDialog(
                title=ft.Text("خطأ"),
                content=ft.Text(f"خطأ في قاعدة البيانات: {err}"),
                actions=[
                ],
                actions_alignment=ft.MainAxisAlignment.END,
                bgcolor=red
            )
            page.overlay.append(alert_dialog)
            alert_dialog.open = True
            page.update()

    main_rect = Container(
        expand=True,
        width=345,
        height=150,
        bgcolor=gray,
        border_radius=24,
        alignment=alignment.center,
        margin=margin.only(top=100),
        content=Column(
            controls=[
                Container(
                    width=301,
                    bgcolor=white,
                    border_radius=24,
                    alignment=alignment.center,
                    content=customer_dropdown
                ),
            ],
            spacing=50,
            alignment=MainAxisAlignment.CENTER,
        )
    )

    sec_rect = Container(
        width=300,
        height=60,
        bgcolor=blue,
        border_radius=24,
        alignment=alignment.center,
        margin=margin.only(top=50),
        content=Row(
            [
                Text(
                    "البحث عن فاتورة",
                    color=white,
                    size=24,
                    weight=FontWeight.BOLD,
                )
            ],
            alignment=MainAxisAlignment.CENTER
        )
    )

    b1 = ElevatedButton(
        content=Text("عرض", size=18, weight=FontWeight.BOLD),
        width=150,
        style=ButtonStyle(bgcolor=blue, color=white, padding=15),
        on_click=lambda e: show_invoices(e),
    )

    b2 = ElevatedButton(
        content=Text("حذف الكل", size=18, weight=FontWeight.BOLD),
        width=150,
        style=ButtonStyle(bgcolor=blue, color=white, padding=15),
        on_click=lambda e: delete_all_invoices(e),
    )

    page_content = Column(
        controls=[
            Stack(controls=[main_rect, Container(content=sec_rect, margin=margin.only(top=-30))], alignment=alignment.top_center),
            Row([b1, b2], alignment=MainAxisAlignment.CENTER),
            Container(
                content=cards_column,
                height=300,
                width=345,
                bgcolor="#F0F0F0",
                border_radius=24,
                padding=10,
                margin=margin.only(top=20)
            )
        ],
        spacing=20,
        expand=True,
        alignment=MainAxisAlignment.CENTER,
        horizontal_alignment=CrossAxisAlignment.CENTER,
    )
    return page_content




def create_page_add_item(store_names, page):
    # إنشاء قائمة "نوع الصنف" مع إضافة "نوع الصنف" كخيار افتراضي
    store_type_dropdown = create_dropdown(
        options=["نوع الصنف", "ادوية", "مستلزمات", "اخر"],
        hint_text="نوع الصنف",
        default_value="نوع الصنف",
        page=page
    )

    # إنشاء قائمة "اختر المخزن"
    store_dropdown = create_dropdown(
        options=store_names,
        hint_text="اختر المخزن",
        default_value="اختر المخزن",
        page=page
    )

    def add_item(e, page):
        item = item_name.value.strip()
        item_type = store_type_dropdown.value
        selected_store_name = store_dropdown.value

        if not item or item_type == "نوع الصنف" or selected_store_name == "اختر المخزن":
            alert_dialog = ft.AlertDialog(
                title=ft.Text("خطأ"),
                content=ft.Text("يرجى ملء كل الحقول"),
                actions=[
                ],
                actions_alignment=ft.MainAxisAlignment.END,
                bgcolor=red
            )
            page.overlay.append(alert_dialog)
            alert_dialog.open = True
            page.update()
            return

        cursor.execute("SELECT id FROM store WHERE store_name = ?", (selected_store_name,))
        result = cursor.fetchone()
        if result:
            store_id = result[0]
            cursor.execute("INSERT INTO items (item_name, item_type, store_id) VALUES (?, ?, ?)",
                          (item, item_type, store_id))
            conn.commit()
            alert_dialog = ft.AlertDialog(
                title=ft.Text("نجاح"),
                content=ft.Text("تمت إضافة الصنف بنجاح"),
                actions=[
                ],
                actions_alignment=ft.MainAxisAlignment.END,
                bgcolor=green
            )
            page.overlay.append(alert_dialog)
            alert_dialog.open = True
            # إعادة تعيين الحقول
            item_name.value = ""
            store_type_dropdown.value = "نوع الصنف"
            store_dropdown.value = "اختر المخزن"
        else:
            alert_dialog = ft.AlertDialog(
                title=ft.Text("خطأ"),
                content=ft.Text("لم يتم العثور على المخزن"),
                actions=[
                ],
                actions_alignment=ft.MainAxisAlignment.END,
                bgcolor=red
            )
            page.overlay.append(alert_dialog)
            alert_dialog.open = True

        page.update()

    def delete_item(e, page):
        item = item_name.value.strip()
        item_type = store_type_dropdown.value
        selected_store_name = store_dropdown.value

        if not item or item_type == "نوع الصنف" or selected_store_name == "اختر المخزن":
            alert_dialog = ft.AlertDialog(
                title=ft.Text("خطأ"),
                content=ft.Text("يرجى ملء كل الحقول للحذف"),
                actions=[
                ],
                actions_alignment=ft.MainAxisAlignment.END,
                bgcolor=red
            )
            page.overlay.append(alert_dialog)
            alert_dialog.open = True
            page.update()
            return

        try:
            cursor.execute("SELECT id FROM store WHERE store_name = ?", (selected_store_name,))
            result = cursor.fetchone()
            if not result:
                alert_dialog = ft.AlertDialog(
                    title=ft.Text("خطأ"),
                    content=ft.Text("لم يتم العثور على المخزن"),
                    actions=[
                    ],
                    actions_alignment=ft.MainAxisAlignment.END,
                    bgcolor=red
                )
                page.overlay.append(alert_dialog)
                alert_dialog.open = True
                page.update()
                return

            store_id = result[0]
            cursor.execute(
                "DELETE FROM items WHERE item_name = ? AND item_type = ? AND store_id = ?",
                (item, item_type, store_id)
            )
            if cursor.rowcount == 0:
                alert_dialog = ft.AlertDialog(
                    title=ft.Text("خطأ"),
                    content=ft.Text("لم يتم العثور على الصنف للحذف"),
                    actions=[
                    ],
                    actions_alignment=ft.MainAxisAlignment.END,
                    bgcolor=red
                )
            else:
                conn.commit()
                alert_dialog = ft.AlertDialog(
                    title=ft.Text("نجاح"),
                    content=ft.Text("تم حذف الصنف بنجاح"),
                    actions=[
                    ],
                    actions_alignment=ft.MainAxisAlignment.END,
                    bgcolor=green
                )
                # إعادة تعيين الحقول
                item_name.value = ""
                store_type_dropdown.value = "نوع الصنف"
                store_dropdown.value = "اختر المخزن"

            page.overlay.append(alert_dialog)
            alert_dialog.open = True
            page.update()

        except sqlite3.Error as err:
            alert_dialog = ft.AlertDialog(
                title=ft.Text("خطأ"),
                content=ft.Text(f"خطأ في قاعدة البيانات: {err}"),
                actions=[
                ],
                actions_alignment=ft.MainAxisAlignment.END,
                bgcolor=red
            )
            page.overlay.append(alert_dialog)
            alert_dialog.open = True
            page.update()

    main_rect = Container(
        expand=True,
        width=345,
        height=400,
        bgcolor=gray,
        border_radius=24,
        alignment=alignment.center,
        margin=margin.only(top=100),
        content=Column(
            controls=[
                Container(
                    width=301,
                    bgcolor=white,
                    border_radius=24,
                    alignment=alignment.center,
                    margin=margin.only(top=0),
                    content=item_name
                ),
                Container(
                    width=301,
                    bgcolor=white,
                    border_radius=24,
                    alignment=alignment.center,
                    content=store_type_dropdown
                ),
                Container(
                    width=301,
                    bgcolor=white,
                    border_radius=24,
                    alignment=alignment.center,
                    content=store_dropdown
                ),
            ],
            spacing=63,
            alignment=MainAxisAlignment.CENTER,
        )
    )
    sec_rect = Container(
        width=300,
        height=60,
        bgcolor=blue,
        border_radius=24,
        alignment=alignment.center,
        margin=margin.only(top=50),
        content=Row(
            [
                Text(
                    "اضف صنفاً!",
                    color=white,
                    size=24,
                    weight=FontWeight.BOLD,
                )
            ],
            alignment=MainAxisAlignment.CENTER
        )
    )
    b1 = ElevatedButton(
        content=Text("اضافة", size=18, weight=FontWeight.BOLD),
        width=150,
        style=ButtonStyle(bgcolor=blue, color=white, padding=15),
        on_click=lambda e: add_item(e, page)
    )
    b2 = ElevatedButton(
        content=Text("حذف", size=18, weight=FontWeight.BOLD),
        width=150,
        style=ButtonStyle(bgcolor=blue, color=white, padding=15),
        on_click=lambda e: delete_item(e, page)
    )
    page_content = Column(
        controls=[
            Stack(controls=[main_rect, Container(content=sec_rect, margin=margin.only(top=-30))], alignment=alignment.top_center),
            Row([b1, b2], alignment=MainAxisAlignment.CENTER),
        ],
        spacing=10,
        expand=True,
        alignment=MainAxisAlignment.CENTER,
        horizontal_alignment=CrossAxisAlignment.CENTER,
    )
    return page_content

store_name     = TextField(hint_text='اسم المخزن'        , height=48,width=301,border_radius=24,color='black',bgcolor=white,border_color='gray',focused_border_color=blue,text_align=TextAlign.RIGHT,)
store_phone    = TextField(hint_text='هاتف المخزن'       , height=48,width=301,border_radius=24,color='black',bgcolor=white,border_color='gray',focused_border_color=blue,text_align=TextAlign.RIGHT,)
person1_name   = TextField(hint_text='اسم المندوب الاول'       , height=48,width=301,border_radius=24,color='black',bgcolor=white,border_color='gray',focused_border_color=blue,text_align=TextAlign.RIGHT,)
person1_phone  = TextField(hint_text='رقم هاتف المندوب الاول'  , height=48,width=301,border_radius=24,color='black',bgcolor=white,border_color='gray',focused_border_color=blue,text_align=TextAlign.RIGHT,)
person2_name   = TextField(hint_text='اسم المدوب الثاني' , height=48,width=301,border_radius=24,color='black',bgcolor=white,border_color='gray',focused_border_color=blue,text_align=TextAlign.RIGHT,)
person2_phone  = TextField(hint_text='رقم هاتف المندوب الثاني', height=48,width=301,border_radius=24,color='black',bgcolor=white,border_color='gray',focused_border_color=blue,text_align=TextAlign.RIGHT,)
 
def create_page_view_orders(store_names, page):
    cursor.execute("SELECT store_name FROM store")
    store_names = [row[0] for row in cursor.fetchall()]
    store_names.insert(0, "اختر المخزن")

    store_dropdown = create_dropdown(
        options=store_names,
        hint_text="اختر المخزن",
        default_value="اختر المخزن",
        page=page
    )
# def create_dropdown(options, hint_text, default_value, width=301, page=None):

    item_type_dropdown = create_dropdown(
        options=["ادوية", "مستلزمات", "اخر"],
        hint_text="نوع الصنف",
        default_value="نوع الصنف",
        page=page
    )

    cards_column = ft.Column(scroll=ft.ScrollMode.AUTO, spacing=10)

    def show_items(e):
        selected_store = store_dropdown.value
        selected_type = item_type_dropdown.value

        if selected_store == "اختر المخزن":
            alert_dialog = ft.AlertDialog(
                title=ft.Text("خطأ"),
                content=ft.Text("يرجى اختيار المخزن"),
                actions=[
                ],
                actions_alignment=ft.MainAxisAlignment.END,
                bgcolor=red
            )
            page.overlay.append(alert_dialog)
            alert_dialog.open = True
            page.update()
            return

        query = """
            SELECT items.item_name, store.store_name, store.store_phone, 
                store.store_person1_name, store.store_person1phone,
                store.store_person2_name, store.store_person2phone
            FROM items 
            JOIN store ON items.store_id = store.id
            WHERE store.store_name = ? AND items.item_type = ?
        """
        try:
            cursor.execute(query, (selected_store, selected_type))
            rows = cursor.fetchall()
        except sqlite3.Error as err:
            alert_dialog = ft.AlertDialog(
                title=ft.Text("خطأ"),
                content=ft.Text(f"خطأ في قاعدة البيانات: {err}"),
                actions=[
                ],
                actions_alignment=ft.MainAxisAlignment.END,
                bgcolor=red
            )
            page.overlay.append(alert_dialog)
            alert_dialog.open = True
            page.update()
            return

        cards_column.controls.clear()

        if not rows:
            cards_column.controls.append(
                ft.Text("لا توجد أصناف مطابقة", size=18, color="red", text_align=ft.TextAlign.CENTER)
            )
        else:
            # استخراج بيانات المخزن من أول صف
            _, store_name, store_phone, person1_name, person1_phone, person2_name, person2_phone = rows[0]

            # إنشاء بطاقة بيانات المخزن مع أيقونة
            store_fields = [
                ft.Row(
                    controls=[
                        ft.Icon(ft.Icons.STORE, size=24, color="black"),
                        ft.Text(f"المخزن: {store_name}", size=18, weight=ft.FontWeight.BOLD, color="black")
                    ], spacing=5, alignment=ft.MainAxisAlignment.START
                ),
                GestureDetector(
                    on_tap=lambda e: page.launch_url(f"tel:{store_phone}"),
                    content=ft.Text(
                        f"📞 هاتف المخزن: {store_phone}",
                        size=16,
                        color="blue",
                        weight=ft.FontWeight.BOLD
                    )
                ),
                ft.Text(f"المندوب الاول {person1_name}", size=16, color="black"),
                GestureDetector(
                    on_tap=lambda e: page.launch_url(f"tel:{person1_phone}"),
                    content=ft.Text(
                        f"📞 هاتف المندوب: {person1_phone}",
                        size=16,
                        color="blue",
                        weight=ft.FontWeight.BOLD
                    )
                ),
            ]

            if person2_name and person2_name.strip():
                store_fields.append(ft.Text(f"المندوب الثاني: {person2_name}", size=16, color="black"))

            if person2_phone and person2_phone.strip():
                store_fields.append(
                    GestureDetector(
                        on_tap=lambda e: page.launch_url(f"tel:{person2_phone}"),
                        content=ft.Text(
                            f"📞 هاتف المندوب : {person2_phone}",
                            size=16,
                            color="blue",
                            weight=ft.FontWeight.BOLD
                        )
                    )
                )

            store_card = ft.Container(
                content=ft.Card(
                    content=ft.Container(
                        content=ft.Column(
                            store_fields,
                            spacing=5,
                            alignment=ft.MainAxisAlignment.START,
                        ),
                        padding=10,
                        bgcolor="#E0E0E0",  # خلفية رمادية فاتحة للمخزن
                    ),
                    elevation=3,
                    color="white",
                ),
                border_radius=24,  # زوايا بدرجة 24 للتناغم مع الإطار
                margin=ft.margin.only(left=5, right=5, top=5, bottom=10),  # تقليل الهوامش
                bgcolor="white",
            )
            cards_column.controls.append(store_card)

            # إضافة بطاقات الأصناف بلون أخضر
            for item_name, _, _, _, _, _, _ in rows:
                def delete_item(e, item_name=item_name, store_name=store_name, item_type=selected_type):
                    def confirm_delete(e):
                        try:
                            cursor.execute("SELECT id FROM store WHERE store_name = ?", (store_name,))
                            result = cursor.fetchone()
                            if not result:
                                alert_dialog = ft.AlertDialog(
                                    title=ft.Text("خطأ"),
                                    content=ft.Text("لم يتم العثور على المخزن"),
                                    actions=[
                                    ],
                                    actions_alignment=ft.MainAxisAlignment.END,
                                    bgcolor=red
                                )
                                page.overlay.append(alert_dialog)
                                alert_dialog.open = True
                                page.update()
                                return

                            store_id = result[0]
                            cursor.execute(
                                "DELETE FROM items WHERE item_name = ? AND item_type = ? AND store_id = ?",
                                (item_name, item_type, store_id)
                            )
                            if cursor.rowcount == 0:
                                alert_dialog = ft.AlertDialog(
                                    title=ft.Text("خطأ"),
                                    content=ft.Text(f"لم يتم العثور على الصنف '{item_name}'"),
                                    actions=[
                                    ],
                                    actions_alignment=ft.MainAxisAlignment.END,
                                    bgcolor=red
                                )
                            else:
                                conn.commit()
                                alert_dialog = ft.AlertDialog(
                                    title=ft.Text("نجاح"),
                                    content=ft.Text(f"تم حذف الصنف '{item_name}' بنجاح"),
                                    actions=[
                                    ],
                                    actions_alignment=ft.MainAxisAlignment.END,
                                    bgcolor=green
                                )
                                show_items(None)  # إعادة تحميل البطاقات
                            page.overlay.append(alert_dialog)
                            alert_dialog.open = True
                        except sqlite3.Error as err:
                            alert_dialog = ft.AlertDialog(
                                title=ft.Text("خطأ"),
                                content=ft.Text(f"خطأ في قاعدة البيانات: {err}"),
                                actions=[
                                ],
                                actions_alignment=ft.MainAxisAlignment.END,
                                bgcolor=red
                            )
                            page.overlay.append(alert_dialog)
                            alert_dialog.open = True
                        page.update()

                    def cancel_delete(e):
                        page.overlay.pop() if page.overlay else None
                        page.update()

                    alert_dialog = ft.AlertDialog(
                        title=ft.Text("تأكيد الحذف"),
                        content=ft.Text(f"هل أنت متأكد أنك تريد حذف الصنف '{item_name}'؟"),
                        actions=[
                            ft.TextButton("نعم", on_click=confirm_delete),
                            ft.TextButton("لا", on_click=cancel_delete),
                        ],
                        actions_alignment=ft.MainAxisAlignment.END,
                    )
                    page.overlay.append(alert_dialog)
                    alert_dialog.open = True
                    page.update()

                item_card = ft.Container(
                    content=ft.Card(
                        content=ft.Container(
                            content=ft.Row(
                                controls=[
                                    ft.Text(f"الصنف: {item_name}", size=16, weight=ft.FontWeight.BOLD, color="black"),
                                    ft.IconButton(
                                        icon=ft.Icons.DELETE,
                                        icon_color=red,
                                        tooltip="حذف الصنف",
                                        on_click=delete_item,
                                    ),
                                ],
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                            ),
                            padding=10,
                            bgcolor="#7AFAB0",  # خلفية خضراء للأصناف
                        ),
                        elevation=2,
                        color="white",
                    ),
                    border_radius=24,  # زوايا بدرجة 24 للتناغم مع الإطار
                    margin=ft.margin.only(left=5, right=5, top=5, bottom=5),  # تقليل الهوامش
                    bgcolor="white",
                )
                cards_column.controls.append(item_card)

        page.update()

    def delete_all_items(e):
        try:
            cursor.execute("DELETE FROM items")
            conn.commit()
            cards_column.controls.clear()
            alert_dialog = ft.AlertDialog(
                title=ft.Text("نجاح"),
                content=ft.Text("تم حذف جميع الأصناف"),
                actions=[
                ],
                actions_alignment=ft.MainAxisAlignment.END,
                bgcolor=green
            )
            page.overlay.append(alert_dialog)
            alert_dialog.open = True
            page.update()
        except sqlite3.Error as err:
            alert_dialog = ft.AlertDialog(
                title=ft.Text("خطأ"),
                content=ft.Text(f"خطأ في قاعدة البيانات: {err}"),
                actions=[
                ],
                actions_alignment=ft.MainAxisAlignment.END,
                bgcolor=red
            )
            page.overlay.append(alert_dialog)
            alert_dialog.open = True
            page.update()

    main_rect = Container(
        expand=True,
        width=345,
        height=350,
        bgcolor=gray,
        border_radius=24,
        alignment=alignment.center,
        margin=margin.only(top=100),
        content=Column(
            controls=[
                
                Container(
                    width=301,
                    bgcolor=gray,
                    border_radius=24,
                    alignment=alignment.center,
                    content=Text('اختر كيفية عرض الاصناف', height=45, size=28, width=300, weight=FontWeight.BOLD, color=brown, text_align=TextAlign.CENTER)
                ),
                Container(
                    width=301,
                    bgcolor=white,
                    border_radius=24,
                    alignment=alignment.center,
                    content=item_type_dropdown
                ),
                Container(
                    width=301,
                    bgcolor=white,
                    border_radius=24,
                    alignment=alignment.center,
                    content=store_dropdown
                ),
            ],
            spacing=50,
            alignment=MainAxisAlignment.CENTER,
        )
    )
    sec_rect = Container(
        width=300,
        height=60,
        bgcolor=blue,
        border_radius=24,
        alignment=alignment.center,
        margin=margin.only(top=50),
        content=Row(
            [
                Text(
                    "عرض المطلوب!",
                    color=white,
                    size=24,
                    weight=FontWeight.BOLD,
                )
            ],
            alignment=MainAxisAlignment.CENTER
        )
    )
    b1 = ElevatedButton(
        content=Text("عرض", size=18, weight=FontWeight.BOLD),
        width=150,
        style=ButtonStyle(bgcolor=blue, color=white, padding=15),
        on_click=lambda e: show_items(e),
    )
    b2 = ElevatedButton(
        content=Text("حذف", size=18, weight=FontWeight.BOLD),
        width=150,
        style=ButtonStyle(bgcolor=blue, color=white, padding=15),
        on_click=lambda e: delete_all_items(e),
    )
    page_content = Column(
        controls=[
            Stack(controls=[main_rect, Container(content=sec_rect, margin=margin.only(top=-30))], alignment=alignment.top_center),
            Row([b1, b2], alignment=MainAxisAlignment.CENTER),
            Container(
                content=cards_column,
                height=300,
                width=345,
                bgcolor="#F0F0F0",
                border_radius=24,
                padding=10,
                margin=margin.only(top=20)
            )
        ],
        spacing=20,
        expand=True,
        alignment=MainAxisAlignment.CENTER,
        horizontal_alignment=CrossAxisAlignment.CENTER,
    )
    return page_content
 



# دالة مساعدة لتحديث قوائم المخازن
def update_store_names(cursor):
    cursor.execute("SELECT store_name FROM store")
    store_names = [row[0] for row in cursor.fetchall()]
    store_names.insert(0, "اختر المخزن")
    return store_names

# تعديل دالة create_page_stores_management
def create_page_stores_management(page, pages):
    def add_store_to_db(e, page, pages):
        # التحقق من أن اسم المخزن ليس فارغًا
        if not store_name.value.strip():
            alert_dialog = ft.AlertDialog(
                title=ft.Text("خطأ"),
                content=ft.Text("يرجى إدخال اسم المخزن"),
                actions=[],
                actions_alignment=ft.MainAxisAlignment.END,
                bgcolor=red
            )
            page.overlay.append(alert_dialog)
            alert_dialog.open = True
            page.update()
            return

        # التحقق من وجود اسم المخزن في قاعدة البيانات
        cursor.execute("SELECT id FROM store WHERE store_name = ?", (store_name.value.strip(),))
        if cursor.fetchone():
            alert_dialog = ft.AlertDialog(
                title=ft.Text("خطأ"),
                content=ft.Text(f"اسم المخزن '{store_name.value}' موجود بالفعل! يرجى اختيار اسم آخر."),
                actions=[],
                actions_alignment=ft.MainAxisAlignment.END,
                bgcolor=red
            )
            page.overlay.append(alert_dialog)
            alert_dialog.open = True
            page.update()
            return

        # إضافة المخزن إلى قاعدة البيانات
        try:
            cursor.execute("""
                INSERT INTO store (store_name, store_phone, store_person1_name, store_person1phone, store_person2_name, store_person2phone)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                store_name.value,
                store_phone.value,
                person1_name.value,
                person1_phone.value,
                person2_name.value,
                person2_phone.value
            ))
            conn.commit()
            alert_dialog = ft.AlertDialog(
                title=ft.Text("نجاح"),
                content=ft.Text("تم إضافة المخزن بنجاح!"),
                actions=[],
                actions_alignment=ft.MainAxisAlignment.END,
                bgcolor=green
            )
            page.overlay.append(alert_dialog)
            alert_dialog.open = True

            # إعادة تعيين الحقول
            store_name.value = ""
            store_phone.value = ""
            person1_name.value = ""
            person1_phone.value = ""
            person2_name.value = ""
            person2_phone.value = ""

            # تحديث قوائم المخازن
            store_names = update_store_names(cursor)
            
            # تحديث الصفحات
            pages[0] = create_home_page(store_names, page)  # الحفاظ على الصفحة الرئيسية
            pages[1] = create_page_view_orders(store_names, page)
            pages[2] = create_page_stores_management(page, pages)  # إعادة إنشاء صفحة إدارة المخازن
            
            # إعادة تعيين المحتوى الحالي بناءً على الصفحة المختارة
            content_container.content = pages[page.navigation_bar.selected_index]
            page.update()

        except sqlite3.Error as err:
            alert_dialog = ft.AlertDialog(
                title=ft.Text("خطأ"),
                content=ft.Text(f"خطأ في قاعدة البيانات: {err}"),
                actions=[],
                actions_alignment=ft.MainAxisAlignment.END,
                bgcolor=red
            )
            page.overlay.append(alert_dialog)
            alert_dialog.open = True
            page.update()

    def delete_store_from_db(e, page, pages):
        store_to_delete = store_name.value.strip()

        if not store_to_delete:
            alert_dialog = ft.AlertDialog(
                title=ft.Text("خطأ"),
                content=ft.Text("يرجى إدخال اسم المخزن لحذفه"),
                actions=[],
                actions_alignment=ft.MainAxisAlignment.END,
                bgcolor=red
            )
            page.overlay.append(alert_dialog)
            alert_dialog.open = True
            page.update()
            return

        try:
            cursor.execute("SELECT id FROM store WHERE store_name = ?", (store_to_delete,))
            result = cursor.fetchone()
            if not result:
                alert_dialog = ft.AlertDialog(
                    title=ft.Text("خطأ"),
                    content=ft.Text(f"لم يتم العثور على المخزن '{store_to_delete}'"),
                    actions=[],
                    actions_alignment=ft.MainAxisAlignment.END,
                    bgcolor=red
                )
                page.overlay.append(alert_dialog)
                alert_dialog.open = True
                page.update()
                return

            cursor.execute("DELETE FROM store WHERE store_name = ?", (store_to_delete,))
            if cursor.rowcount == 0:
                alert_dialog = ft.AlertDialog(
                    title=ft.Text("خطأ"),
                    content=ft.Text(f"لم يتم حذف المخزن '{store_to_delete}'"),
                    actions=[],
                    actions_alignment=ft.MainAxisAlignment.END,
                    bgcolor=red
                )
            else:
                conn.commit()
                alert_dialog = ft.AlertDialog(
                    title=ft.Text("نجاح"),
                    content=ft.Text(f"تم حذف المخزن '{store_to_delete}' وجميع الأصناف المرتبطة به بنجاح"),
                    actions=[],
                    actions_alignment=ft.MainAxisAlignment.END,
                    bgcolor=green
                )

                # إعادة تعيين الحقول
                store_name.value = ""
                store_phone.value = ""
                person1_name.value = ""
                person1_phone.value = ""
                person2_name.value = ""
                person2_phone.value = ""

                # تحديث قوائم المخازن
                store_names = update_store_names(cursor)
                
                # تحديث الصفحات
                pages[0] = create_home_page(store_names, page)  # الحفاظ على الصفحة الرئيسية
                pages[1] = create_page_view_orders(store_names, page)
                pages[2] = create_page_stores_management(page, pages)  # إعادة إنشاء صفحة إدارة المخازن
                
                # إعادة تعيين المحتوى الحالي بناءً على الصفحة المختارة
                content_container.content = pages[page.navigation_bar.selected_index]

            page.overlay.append(alert_dialog)
            alert_dialog.open = True
            page.update()

        except sqlite3.Error as err:
            alert_dialog = ft.AlertDialog(
                title=ft.Text("خطأ"),
                content=ft.Text(f"خطأ في قاعدة البيانات: {err}"),
                actions=[],
                actions_alignment=ft.MainAxisAlignment.END,
                bgcolor=red
            )
            page.overlay.append(alert_dialog)
            alert_dialog.open = True
            page.update()

    main_rect = Container(
        expand=True,
        width=345,
        height=400,
        bgcolor=gray,
        border_radius=24,
        alignment=alignment.center,
        margin=margin.only(top=100),
        content=Column(
            controls=[
                Container(
                    width=301,
                    bgcolor=white,
                    border_radius=24,
                    alignment=alignment.center,
                    margin=margin.only(top=0),
                    content=store_name
                ),
                Container(
                    width=301,
                    bgcolor=white,
                    border_radius=24,
                    alignment=alignment.center,
                    content=store_phone
                ),
                Container(
                    width=301,
                    bgcolor=white,
                    border_radius=24,
                    alignment=alignment.center,
                    content=person1_name
                ),
                Container(
                    width=301,
                    bgcolor=white,
                    border_radius=24,
                    alignment=alignment.center,
                    content=person1_phone
                ),
                Container(
                    width=301,
                    bgcolor=white,
                    border_radius=24,
                    alignment=alignment.center,
                    content=person2_name
                ),
                Container(
                    width=301,
                    bgcolor=white,
                    border_radius=24,
                    alignment=alignment.center,
                    content=person2_phone
                ),
            ],
            spacing=15,
            alignment=MainAxisAlignment.CENTER,
        )
    )

    sec_rect = Container(
        width=300,
        height=60,
        bgcolor=blue,
        border_radius=24,
        alignment=alignment.center,
        margin=margin.only(top=50),
        content=Row(
            [
                Text(
                    "اضافة- حذف مخزن!",
                    color=white,
                    size=24,
                    weight=FontWeight.BOLD,
                )
            ],
            alignment=MainAxisAlignment.CENTER
        )
    )

    b1 = ElevatedButton(
        content=Text("اضافة", size=18, weight=FontWeight.BOLD),
        width=150,
        style=ButtonStyle(bgcolor=blue, color=white, padding=15),
        on_click=lambda e: add_store_to_db(e, page, pages)
    )

    b2 = ElevatedButton(
        content=Text("حذف", size=18, weight=FontWeight.BOLD),
        width=150,
        style=ButtonStyle(bgcolor=blue, color=white, padding=15),
        on_click=lambda e: delete_store_from_db(e, page, pages)
    )

    page_content = Column(
        controls=[
            Stack(controls=[main_rect, Container(content=sec_rect, margin=margin.only(top=-30))], alignment=alignment.top_center),
            Row([b1, b2], alignment=MainAxisAlignment.CENTER),
        ],
        spacing=30,
        expand=True,
        alignment=MainAxisAlignment.CENTER,
        horizontal_alignment=CrossAxisAlignment.CENTER,
    )
    return page_content

def create_page_contact(page):
    main_rect = Container(
        expand=True,
        width=345,
        height=450,
        bgcolor=gray,
        border_radius=24,
        alignment=alignment.center,
        margin=margin.only(top=100),
        content=Column(
            controls=[
                Container(
                    width=320,
                    height=45,
                    bgcolor=white,
                    border_radius=24,
                    alignment=alignment.center,
                    margin=margin.only(top=0),
                    content=Row(
                        controls=[
                            Text(
                                'Salah Abdeldaim',
                                size=20,
                                color=brown,
                                weight=FontWeight.BOLD,
                                text_align=TextAlign.LEFT,
                                width=220  # عرض ثابت للنص عشان يبقى في المنتصف
                            ),
                              # فاصل مرن عشان يدفع الأيقونة لأقصى اليمين
                            GestureDetector(
                                on_tap=lambda e: page.launch_url("https://www.facebook.com/share/16dTmEVH9x/"),
                                content=Image(facebook, width=35, height=35)
                            ),
                            Row([Text('', size=5)], alignment=MainAxisAlignment.CENTER)
                        ],
                        alignment=MainAxisAlignment.SPACE_BETWEEN,
                        vertical_alignment=CrossAxisAlignment.CENTER
                    )
                ),
                Container(
                    width=320,
                    height=45,
                    bgcolor=white,
                    border_radius=24,
                    alignment=alignment.center,
                    content=Row(
                        controls=[
                            Text(
                                '01013243393',
                                size=20,
                                color=brown,
                                weight=FontWeight.BOLD,
                                text_align=TextAlign.LEFT,
                                width=220
                            ),
                            
                            GestureDetector(
                                on_tap=lambda e: page.launch_url("https://wa.me/qr/3LLSAO65DGOXP1"),
                                content=Image(whatsapp, width=35, height=35)
                            ),
                            Row([Text('', size=5)], alignment=MainAxisAlignment.CENTER)
                        ],
                        alignment=MainAxisAlignment.SPACE_BETWEEN,
                        vertical_alignment=CrossAxisAlignment.CENTER
                    )
                ),
                Container(
                    width=320,
                    height=45,
                    bgcolor=white,
                    border_radius=24,
                    alignment=alignment.center,
                    content=Row(
                        controls=[
                            Text(
                                'Salah Abdeldaim',
                                size=20,
                                color=brown,
                                weight=FontWeight.BOLD,
                                text_align=TextAlign.LEFT,
                                width=220
                            ),
                            
                            GestureDetector(
                                on_tap=lambda e: page.launch_url("https://www.linkedin.com/in/salah-abdeldaim-226382264?utm_source=share&utm_campaign=share_via&utm_content=profile&utm_medium=android_app"),
                                content=Image(linkedin, width=35, height=35)
                            ),
                            Row([Text('', size=5)], alignment=MainAxisAlignment.CENTER)
                        ],
                        alignment=MainAxisAlignment.SPACE_BETWEEN,
                        vertical_alignment=CrossAxisAlignment.CENTER
                    )
                ),
                Container(
                    width=320,
                    height=45,
                    bgcolor=white,
                    border_radius=24,
                    alignment=alignment.center,
                    margin=margin.only(top=0),
                    content=Row(
                        controls=[
                            
                            Text(
                                'salahabdeldaim609@gmail.com',
                                size=16,
                                color=brown,
                                weight=FontWeight.BOLD,
                                text_align=TextAlign.LEFT,
                                width=250
                            ),
                            Container(expand=True),
                            GestureDetector(
                                on_tap=lambda e: page.launch_url("https://mail.google.com/mail/?view=cm&fs=1&to=salahabdeldaim609@gmail.com"),
                                content=Image(gmail, width=35, height=35)
                            ),
                            Row([Text(' ', size=15)], alignment=MainAxisAlignment.CENTER)
                        ],
                        alignment=MainAxisAlignment.SPACE_BETWEEN,
                        vertical_alignment=CrossAxisAlignment.CENTER
                    )
                ),
            ],
            spacing=55,
            alignment=MainAxisAlignment.CENTER,
        )
    )

    sec_rect = Container(
        width=300,
        height=60,
        bgcolor=blue,
        border_radius=24,
        alignment=alignment.center,
        margin=margin.only(top=40),
        content=Row(
            [
                Text(
                    "تواصل معنا!",
                    color=white,
                    size=24,
                    weight=FontWeight.BOLD,
                )
            ],
            alignment=MainAxisAlignment.CENTER
        )
    )

    page_content = Column(
        controls=[
            Stack(controls=[main_rect, Container(content=sec_rect, margin=margin.only(top=-20))], alignment=alignment.top_center),
        ],
        spacing=20,
        expand=True,
        alignment=MainAxisAlignment.CENTER,
        horizontal_alignment=CrossAxisAlignment.CENTER,
    )
    return page_content
 
 

custom_appbar_title = "مدير المنتجات"

def create_about_page():
    return Column(
        controls=[
            Container(
                content=Text("حول التطبيق", size=30, weight=FontWeight.BOLD, color=brown),
                alignment=alignment.center,
                padding=padding.symmetric(vertical=20)
            ),
            Card(
                content=Column(
                    controls=[
                        ListTile(
                            leading=Icon(name=ft.Icons.APP_SETTINGS_ALT, color=brown),
                            title=Text("اسم التطبيق", weight=FontWeight.BOLD),
                            subtitle=Text("Orx App")
                        ),
                        Divider(),
                        ListTile(
                            leading=Icon(name=Icons.NUMBERS, color=brown),
                            title=Text("الإصدار", weight=FontWeight.BOLD),
                            subtitle=Text("1.0.0")
                        ),
                        Divider(),
                        ListTile(
                            leading=Icon(name=ft.Icons.PERSON, color=brown),
                            title=Text("المطور", weight=FontWeight.BOLD),
                            subtitle=Text("Salah Abdeldaim")
                        ),
                        Divider(),
                        ListTile(
                            leading=Icon(name=ft.Icons.COPYRIGHT, color=brown),
                            title=Text("حقوق النشر", weight=FontWeight.BOLD),
                            subtitle=Text("© 2025 Orx. جميع الحقوق محفوظة.")
                        ),
                    ],
                    spacing=5,
                    expand=True
                ),
                elevation=3,
                margin=10,
                shadow_color=gray,
            )
        ],
        alignment=MainAxisAlignment.CENTER,
        horizontal_alignment=CrossAxisAlignment.CENTER,
        spacing=10,
        scroll=ScrollMode.AUTO
    )
 
def create_help_page(page: Page):
    return Column(
        controls=[
            Container(
                content=Text("نحن هنا لمساعدتك", size=30, weight=FontWeight.BOLD, color="brown"),
                alignment=alignment.center,
                padding=padding.symmetric(vertical=10)
            ),
            Container(
                content=Text(
                    """دليل صفحات تطبيق Orx

يحتوي تطبيق Orx على مجموعة من الصفحات المصممة لتسهيل إدارة المخازن والأصناف والعملاء والفواتير. فيما يلي وصف وشرح لكل صفحة:

صفحة إضافة صنف:

تتيح لك هذه الصفحة إضافة عنصر جديد ترغب في تتبعه لاحقًا، مع إمكانية تحديد تفاصيل مثل اسم الصنف، الكمية، والمخزن المرتبط. يمكنك أيضًا حذف أي صنف لم تعد بحاجة إليه بسهولة.

صفحة عرض المطلوب:

تعرض هذه الصفحة قائمة بجميع الأصناف التي تم إدخالها، مع تفاصيل المخزن المرتبط بكل صنف. تساعدك هذه الصفحة في متابعة الأصناف بدقة ومراجعة حالة المخزون بسرعة.

صفحة إضافة مخزن;

تمكنك هذه الصفحة من إضافة مخزن جديد لتخزين الأصناف، مع تحديد اسم المخزن وتفاصيله. كما يمكنك حذف مخزن لم تعد بحاجة إليه، مما يسهل تنظيم المخازن.

صفحة اطلب لعميل:

توفر هذه الصفحة واجهة لإضافة طلبات جديدة (صنف ستوفره لعميل) . يمكنك أيضًا البحث عن عميل معين أو حذف بيانات عميل غير نشط.

صفحة الفواتير الشهرية:

تعرض هذه الصفحة قائمة بالفواتير الشهرية المسجلة (عميل يقوم بشراء منتجات ما بشكل دوري)، مع تفاصيل مثل اسم العميل، والأصناف المرتبطة. يمكنك إضافة فاتورة جديدة أو مراجعة الفواتير السابقة لتتبع المعاملات.

صفحة تواصل معنا:

تحتوي هذه الصفحة على روابط مباشرة للتواصل مع فريق الدعم عبر منصات مثل واتساب، فيسبوك، لينكدإن، أو البريد الإلكتروني. تتيح لك طلب المساعدة أو تقديم الاقتراحات بسهولة.

صفحة حول التطبيق:

تقدم هذه الصفحة معلومات أساسية عن تطبيق Orx، بما في ذلك الإصدار الحالي، الشركة المطورة (Salah Abdeldaim)، ومعلومات حقوق الطبع والنشر. تساعدك على فهم خلفية التطبيق.

صفحة المساعدة:

توفر هذه الصفحة إرشادات وأسئلة شائعة لتسهيل استخدام التطبيق. تحتوي على نصائح حول كيفية إضافة الأصناف، إدارة المخازن، أو حل المشكلات الشائعة.



ملاحظات:





- جميع الصفحات تدعم اللغة العربية بشكل كامل مع واجهة مستخدم بسيطة وسهلة الاستخدام.



- يمكن التنقل بين الصفحات باستخدام شريط التنقل السفلي أو قائمة الخيارات.



- للحصول على دعم إضافي، راجع صفحة "تواصل معنا" أو "المساعدة".""",
                    size=18,
                    text_align="right"
                ),
                padding=20
            ),
            # النص التوضيحي قبل الواتساب
            Container(
                alignment=alignment.center,
                padding=padding.only(bottom=10),
                content=Text("إذا واجهتك اي مشكلة يرجى التواصل :", size=20, weight=FontWeight.BOLD, color=brown)
            ),
            # حاوية رقم الواتساب
            Container(
                alignment=alignment.center,
                content=Container(
                    width=320,
                    height=45,
                    bgcolor=white,
                    border_radius=24,
                    alignment=alignment.center,
                    content=Row(
                        controls=[
                            GestureDetector(
                                on_tap=lambda e: page.launch_url("https://wa.me/qr/3LLSAO65DGOXP1"),
                                content=Image(whatsapp, width=35, height=35)
                            ),
                            Text('01013243393', size=20, color=brown, weight=FontWeight.BOLD, text_align=TextAlign.RIGHT)
                        ],
                        alignment=MainAxisAlignment.CENTER,
                        vertical_alignment=CrossAxisAlignment.CENTER
                    )
                )
            )
        ]
    )
 
def create_settings_page(page: Page):
    global custom_appbar_title

    def on_dark_mode_change(e):
        mode = e.control.value
        page.theme_mode = ft.ThemeMode.DARK if mode else ft.ThemeMode.LIGHT
        page.update()

    def on_title_change(e):
        global custom_appbar_title
        custom_appbar_title = e.control.value
        page.appbar.title.value = custom_appbar_title
        # تحديث العنوان في قاعدة البيانات
        cursor.execute("SELECT id FROM settings WHERE id = ?", (1,))
        if not cursor.fetchone():
            cursor.execute("INSERT INTO settings (id, app_title) VALUES (?, ?)", (1, custom_appbar_title))
        else:
            cursor.execute("UPDATE settings SET app_title = ? WHERE id = ?", (custom_appbar_title, 1))
        conn.commit()
        page.update()
        

    dark_mode_switch = Switch(value=False, on_change=on_dark_mode_change)
    dark_mode_text = Text("الوضع الليلي", weight=FontWeight.BOLD)

    
    title_input = TextField(
    label="تعديل عنوان التطبيق",
    hint_text="أدخل عنوانًا جديدًا",
    value=custom_appbar_title,
    on_change=on_title_change,
    height=48,
    width=301,
    border_radius=24,
    color='black',             # لون النص داخل الحقل
    bgcolor=white,                # لون خلفية الحقل (منسجم مع الوضع الليلي)
    border_color='gray',         # لون الحدود العادي
    focused_border_color=blue,     # عند التركيز على الحقل
    text_align=TextAlign.RIGHT,    # محاذاة النص
    content_padding=padding.only(right=10),  # مسافة داخلية
    hint_style=TextStyle(color=gray2),            # لون التلميح
    )
    title_row = Row(
    controls=[title_input],
    alignment=MainAxisAlignment.CENTER
)


    switchs_column = Column(
        controls=[dark_mode_switch],
        spacing=10,
        horizontal_alignment=CrossAxisAlignment.START
    )
    texts_column = Column(
        controls=[dark_mode_text],
        spacing=25,
        horizontal_alignment=CrossAxisAlignment.START,
        width=150
    )

    setting_row = Row(
        controls=[texts_column, switchs_column],
        alignment=MainAxisAlignment.CENTER
    )

    return Column(
        controls=[
            Container(
                content=Text("الإعدادات", size=28, weight=FontWeight.BOLD, color=brown),
                alignment=alignment.center,
                padding=padding.symmetric(vertical=20)
            ),
            Card(
                content=Column(
                    controls=[
                        setting_row,title_row
                    ],
                    spacing=20,
                    alignment=MainAxisAlignment.CENTER
                ),
                elevation=3,
                margin=10,
                shadow_color=gray,
                width=370,
                height=400,
            )
        ],
        alignment=MainAxisAlignment.CENTER,
        horizontal_alignment=CrossAxisAlignment.CENTER,
        scroll=ScrollMode.AUTO
    )

def main(page: Page):
    page.theme_mode = ft.ThemeMode.LIGHT

    cursor.execute("SELECT store_name FROM store")
    store_names = [row[0] for row in cursor.fetchall()]
    store_names.insert(0, "اختر المخزن")

    # استرجاع العنوان من قاعدة البيانات
    cursor.execute("SELECT app_title FROM settings WHERE id = ?", (1,))
    result = cursor.fetchone()
    global custom_appbar_title
    custom_appbar_title = result[0] if result else "مدير المنتجات"  # القيمة الافتراضية إذا لم يوجد سجل

    cursor.execute("SELECT store_name FROM store")
    store_names = [row[0] for row in cursor.fetchall()]
    store_names.insert(0, "اختر المخزن")

    page.title = 'Orx'
    page.window.width = 412
    page.window.height = 800
    page.window.top = 2
    page.window.left = 1000
    page.window.resizable = False
    page.bgcolor = yellow
    page.vertical_alignment = MainAxisAlignment.CENTER
    page.horizontal_alignment = CrossAxisAlignment.CENTER
    page.scroll = ScrollMode.AUTO
    page.rtl = True

    # إنشاء قائمة الصفحات
    pages = [
        create_home_page(store_names, page),
        create_page_view_orders(store_names, page),
        None,
        create_page_contact(page),
    ]

    global content_container
    content_container = Container(expand=True)

    pages[2] = create_page_stores_management(page, pages)

    # تعديل استدعاء go_back في AppBar لتمرير page و pages
    page.appbar = AppBar(
        bgcolor=brown,
        title=Text(custom_appbar_title, color=white, weight=FontWeight.BOLD),
        center_title=True,
        leading=IconButton(
            icon=Icons.ARROW_BACK,
            on_click=lambda e: go_back(page, pages),  # تمرير page و pages
            icon_color=white,
        ),
        leading_width=50,
        actions=[
            PopupMenuButton(
                icon=ft.Icons.SETTINGS,
                icon_color=white,
                tooltip="Settings",
                items=[
                    PopupMenuItem(
                        text="Settings",
                        icon=ft.Icons.SETTINGS,
                        on_click=lambda e: show_popup_page(create_settings_page(page), page)
                    ),
                    PopupMenuItem(),
                    PopupMenuItem(
                        text="About",
                        icon=ft.Icons.INFO,
                        on_click=lambda e: show_popup_page(create_about_page(), page)
                    ),
                    PopupMenuItem(),
                    PopupMenuItem(
                        text="Help",
                        icon=ft.Icons.HELP,
                        on_click=lambda e: show_popup_page(create_help_page(page), page)
                    ),
                ]
            )
        ]
    )

    # تعديل استدعاء on_nav_change لتمرير page و pages
    page.navigation_bar = CupertinoNavigationBar(
        bgcolor=brown,
        inactive_color=white,
        active_color=blue,
        height=60,
        destinations=[
            NavigationBarDestination(icon=Icons.HOME, label="الصفحة الرئيسية"),
            NavigationBarDestination(icon=Icons.VIEW_LIST, label="عرض المطلوب"),
            NavigationBarDestination(icon=Icons.STORE, label="ادارة المخازن"),
            NavigationBarDestination(icon=Icons.CONTACT_MAIL, label="تواصل معنا"),
        ],
        on_change=lambda e: on_nav_change(e, page, pages),  # تمرير page و pages
    )

    content_container.content = pages[0]
    page.add(content_container)
    page.update()

    def on_close(e):
        conn.close()
    page.on_close = on_close

ft.app(main, assets_dir="assets")

