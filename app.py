import streamlit as st

st.set_page_config(page_title="Reading List", page_icon="📚")

# ส่วนซ่อน UI ที่ไม่จำเป็น
st.markdown(
    """
    <style>
    [data-testid="stSidebar"], [data-testid="stToolbar"], [data-testid="stDecoration"] {
        display: none;
    }
    #MainMenu, header, footer {
        visibility: hidden;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ส่วน ตัวสถานะเริ่มต้น
if "books" not in st.session_state:
    st.session_state.books = [
        {"id": "B001", "title": "Atomic Habits", "author": "James Clear", "status": "อ่านแล้ว"},
        {"id": "B002", "title": "Deep Work", "author": "Cal Newport", "status": "ยังไม่อ่าน"},
        {"id": "B003", "title": "Python Basics", "author": "John Smith", "status": "ยังไม่อ่าน"},
    ]

if "deleted_books" not in st.session_state:
    st.session_state.deleted_books = []

# ส่วน ฟังก์ชันช่วยเหลือ
def find_book_index(book_id):
    book_id = book_id.lower()
    for i in range(len(st.session_state.books)):
        if st.session_state.books[i]["id"].lower() == book_id:
            return i
    return -1


def linear_search(keyword, mode):
    result = []
    keyword = keyword.lower().strip()

    for book in st.session_state.books:
        if mode == "id":
            if keyword in book["id"].lower():
                result.append(book)
        else:
            if keyword in book["title"].lower():
                result.append(book)

    return result


def insertion_sort_books(book_list):
    sorted_books = book_list.copy()

    for i in range(1, len(sorted_books)):
        key = sorted_books[i]
        j = i - 1

        while j >= 0 and sorted_books[j]["title"].lower() > key["title"].lower():
            sorted_books[j + 1] = sorted_books[j]
            j -= 1

        sorted_books[j + 1] = key

    return sorted_books

# UI หลัก
st.title("📚 Smart Reading List Management System")
st.write("ระบบจัดการรายการหนังสือและสถานะการอ่าน")

menu = st.selectbox(
    "เลือกเมนู",
    ["แสดงข้อมูลหนังสือ", "เพิ่มหนังสือ", "แก้ไขหนังสือ", "ลบหนังสือ", "ค้นหาหนังสือ", "Undo การลบ"],
)

# ส่วน แสดงข้อมูล
if menu == "แสดงข้อมูลหนังสือ":
    st.subheader("📖 รายการหนังสือ")

    sort_choice = st.radio("การแสดงผล", ["ปกติ", "เรียงตามชื่อหนังสือ"])

    if len(st.session_state.books) == 0:
        st.warning("ไม่มีข้อมูลหนังสือ")
    else:
        show_books = (
            insertion_sort_books(st.session_state.books)
            if sort_choice == "เรียงตามชื่อหนังสือ"
            else st.session_state.books
        )

        st.dataframe(show_books, use_container_width=True)

        st.info(f"จำนวนหนังสือทั้งหมด: {len(show_books)} เล่ม")

# ส่วน เพิ่มหนังสือ
elif menu == "เพิ่มหนังสือ":
    st.subheader("➕ เพิ่มข้อมูลหนังสือ")

    book_id = st.text_input("รหัสหนังสือ")
    title = st.text_input("ชื่อหนังสือ")
    author = st.text_input("ผู้เขียน")
    status = st.selectbox("สถานะการอ่าน", ["ยังไม่อ่าน", "อ่านแล้ว"])

    if st.button("เพิ่ม"):
        book_id = book_id.strip().upper()

        if book_id == "" or title == "" or author == "":
            st.error("กรุณากรอกข้อมูลให้ครบ")
        elif find_book_index(book_id) != -1:
            st.error("รหัสหนังสือซ้ำ")
        else:
            st.session_state.books.append({
                "id": book_id,
                "title": title.strip(),
                "author": author.strip(),
                "status": status,
            })
            st.success("เพิ่มหนังสือเรียบร้อย")
            st.rerun()

# ---------------------------
# ส่วน แก้ไข
# ---------------------------
elif menu == "แก้ไขหนังสือ":
    st.subheader("✏️ แก้ไขข้อมูลหนังสือ")

    if not st.session_state.books:
        st.warning("ไม่มีข้อมูลหนังสือ")
    else:
        book_ids = [b["id"] for b in st.session_state.books]
        selected_id = st.selectbox("เลือกรหัสหนังสือ", book_ids)

        index = find_book_index(selected_id)

        if index != -1:
            book = st.session_state.books[index]

            new_id = st.text_input("รหัสใหม่", value=book["id"])
            new_title = st.text_input("ชื่อใหม่", value=book["title"])
            new_author = st.text_input("ผู้เขียนใหม่", value=book["author"])
            new_status = st.selectbox(
                "สถานะ", ["ยังไม่อ่าน", "อ่านแล้ว"],
                index=0 if book["status"] == "ยังไม่อ่าน" else 1
            )

            if st.button("บันทึก"):
                new_id = new_id.strip().upper()

                if new_id == "" or new_title == "" or new_author == "":
                    st.error("กรุณากรอกข้อมูลให้ครบ")
                else:
                    check = find_book_index(new_id)
                    if check != -1 and check != index:
                        st.error("รหัสซ้ำ")
                    else:
                        st.session_state.books[index] = {
                            "id": new_id,
                            "title": new_title.strip(),
                            "author": new_author.strip(),
                            "status": new_status,
                        }
                        st.success("แก้ไขเรียบร้อย")
                        st.rerun()

# ---------------------------
# ลบ
# ---------------------------
elif menu == "ลบหนังสือ":
    st.subheader("🗑️ ลบข้อมูลหนังสือ")

    if not st.session_state.books:
        st.warning("ไม่มีข้อมูลหนังสือ")
    else:
        book_ids = [b["id"] for b in st.session_state.books]
        selected_id = st.selectbox("เลือกหนังสือ", book_ids)

        if st.button("ลบ"):
            index = find_book_index(selected_id)

            if index != -1:
                deleted = st.session_state.books.pop(index)
                st.session_state.deleted_books.append(deleted)
                st.success("ลบเรียบร้อย")
                st.rerun()

# ---------------------------
# ส่วน ค้นหา
# ---------------------------
elif menu == "ค้นหาหนังสือ":
    st.subheader("🔍 ค้นหาหนังสือ")

    search_type = st.radio("ค้นหาจาก", ["รหัสหนังสือ", "ชื่อหนังสือ"])
    keyword = st.text_input("พิมพ์คำค้นหา")

    if keyword:
        result = linear_search(keyword, "id" if search_type == "รหัสหนังสือ" else "title")

        if result:
            st.success(f"พบ {len(result)} รายการ")
            st.dataframe(result, use_container_width=True)
        else:
            st.warning("ไม่พบข้อมูล")

# ---------------------------
# ส่วน UNDO การลบ
# ---------------------------
elif menu == "Undo การลบ":
    st.subheader("↩️ Undo การลบ")

    if not st.session_state.deleted_books:
        st.warning("ไม่มีข้อมูลที่ลบไว้")
    else:
        last = st.session_state.deleted_books[-1]
        st.write("รายการล่าสุด:")
        st.json(last)

        if st.button("Undo"):
            last_book = st.session_state.deleted_books.pop()

            if find_book_index(last_book["id"]) == -1:
                st.session_state.books.append(last_book)
                st.success("กู้คืนสำเร็จ")
                st.rerun()
            else:
                st.error("กู้คืนไม่ได้ (ID ซ้ำ)")
                st.session_state.deleted_books.append(last_book)
