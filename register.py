# Fix encoding for Windows console
import sys
import io
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
import random
import string
import json
import os
from datetime import datetime

def generate_random_email():
    """Tạo email ngẫu nhiên"""
    random_string = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
    return f"test_{random_string}@example.com"

def generate_random_name():
    """Tạo tên ngẫu nhiên"""
    random_string = ''.join(random.choices(string.ascii_lowercase, k=6))
    return f"User_{random_string}"

def load_config():
    """Đọc cấu hình từ file config.json"""
    config_file = "config.json"
    if os.path.exists(config_file):
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            pass
    # Tạo config mặc định
    default_config = {
        "coupon": "damuatdh",
        "name": None,
        "email": None,
        "wait_timeout": 10,
        "fast_mode": True
    }
    save_config(default_config)
    return default_config

def save_config(config):
    """Lưu cấu hình vào file config.json"""
    try:
        with open("config.json", 'w', encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Không thể lưu config: {e}")

def save_registration_info(name, email, coupon, status="unknown"):
    """Lưu thông tin đăng ký vào file"""
    info = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "name": name,
        "email": email,
        "coupon": coupon,
        "status": status
    }
    
    # Lưu vào file JSON
    history_file = "registration_history.json"
    history = []
    
    if os.path.exists(history_file):
        try:
            with open(history_file, 'r', encoding='utf-8') as f:
                history = json.load(f)
        except:
            pass
    
    history.append(info)
    
    try:
        with open(history_file, 'w', encoding='utf-8') as f:
            json.dump(history, f, ensure_ascii=False, indent=2)
        print(f"✓ Đã lưu thông tin vào {history_file}")
    except Exception as e:
        print(f"⚠ Không thể lưu thông tin: {e}")

def register_account(name=None, email=None, coupon=None, fast_mode=True):
    """
    Tự động đăng ký tài khoản trên python1.pyan.vn
    
    Args:
        name: Tên người dùng (nếu None sẽ tự động tạo hoặc đọc từ config)
        email: Email (nếu None sẽ tự động tạo hoặc đọc từ config)
        coupon: Mã coupon (nếu None sẽ đọc từ config)
        fast_mode: Chế độ nhanh (giảm thời gian chờ)
    """
    # Đọc config
    config = load_config()
    if coupon is None:
        coupon = config.get("coupon", "damuatdh")
    if name is None:
        name = config.get("name")
    if email is None:
        email = config.get("email")
    fast_mode = config.get("fast_mode", fast_mode)
    
    # Cấu hình Chrome options - tối ưu cho tốc độ
    chrome_options = Options()
    # Bỏ comment dòng dưới nếu muốn chạy ở chế độ headless (không hiển thị trình duyệt)
    # chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    if fast_mode:
        # Tắt hình ảnh để tải nhanh hơn (chỉ trong fast mode)
        prefs = {"profile.managed_default_content_settings.images": 2}
        chrome_options.add_experimental_option("prefs", prefs)
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    
    # Tối ưu page load strategy
    chrome_options.page_load_strategy = 'eager'  # Không chờ tất cả resources tải xong
    
    # Khởi tạo WebDriver
    # Sử dụng ChromeDriver tự động (nếu đã cài webdriver-manager)
    # Hoặc chỉ định đường dẫn ChromeDriver thủ công
    try:
        from webdriver_manager.chrome import ChromeDriverManager
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
    except ImportError:
        # Nếu chưa cài webdriver-manager, sử dụng ChromeDriver từ PATH
        driver = webdriver.Chrome(options=chrome_options)
    
    try:
        print("Đang truy cập trang web...")
        driver.get('https://python1.pyan.vn/')
        
        # Chờ trang tải
        wait = WebDriverWait(driver, 10)
        
        # Tìm và click vào nút "Đăng Ký Ngay"
        print("Đang tìm nút Đăng Ký...")
        try:
            # Thử tìm bằng link text
            register_button = wait.until(
                EC.element_to_be_clickable((By.LINK_TEXT, "Đăng Ký Ngay"))
            )
        except:
            # Nếu không tìm thấy, thử tìm bằng partial link text
            try:
                register_button = wait.until(
                    EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "Đăng Ký"))
                )
            except:
                # Thử tìm bằng XPath
                register_button = wait.until(
                    EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Đăng Ký')]"))
                )
        
        register_button.click()
        print("Đã click vào nút Đăng Ký")
        # Chờ form xuất hiện thay vì sleep cố định
        if fast_mode:
            wait.until(EC.presence_of_element_located((By.TAG_NAME, "input")))
        else:
            time.sleep(2)
        
        # Tạo thông tin nếu chưa có
        if not name:
            name = generate_random_name()
        if not email:
            email = generate_random_email()
        
        print(f"Đang nhập thông tin:")
        print(f"  - Tên: {name}")
        print(f"  - Email: {email}")
        print(f"  - Coupon: {coupon}")
        
        # Tìm và điền form đăng ký
        # Thử nhiều cách tìm input field
        name_input = None
        email_input = None
        coupon_input = None
        
        # Tìm trường tên
        try:
            name_input = wait.until(EC.presence_of_element_located((By.NAME, "name")))
        except:
            try:
                name_input = wait.until(EC.presence_of_element_located((By.ID, "name")))
            except:
                try:
                    name_input = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Tên' or @placeholder='Họ tên' or @placeholder='Name']")))
                except:
                    name_input = driver.find_element(By.XPATH, "//input[@type='text'][1]")
        
        name_input.clear()
        name_input.send_keys(name)
        print("✓ Đã nhập tên")
        
        # Tìm trường email
        try:
            email_input = wait.until(EC.presence_of_element_located((By.NAME, "email")))
        except:
            try:
                email_input = wait.until(EC.presence_of_element_located((By.ID, "email")))
            except:
                try:
                    email_input = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='email']")))
                except:
                    email_input = driver.find_element(By.XPATH, "//input[@type='email']")
        
        email_input.clear()
        email_input.send_keys(email)
        print("✓ Đã nhập email")
        
        # Tìm trường coupon - thử nhiều cách
        coupon_input = None
        try:
            # Thử tìm bằng name
            coupon_input = wait.until(EC.presence_of_element_located((By.NAME, "coupon")))
        except:
            try:
                # Thử tìm bằng ID
                coupon_input = wait.until(EC.presence_of_element_located((By.ID, "coupon")))
            except:
                try:
                    # Thử tìm bằng placeholder
                    coupon_input = wait.until(EC.presence_of_element_located((By.XPATH, "//input[contains(@placeholder, 'Coupon') or contains(@placeholder, 'coupon') or contains(@placeholder, 'Mã')]")))
                except:
                    try:
                        # Thử tìm bằng name/id chứa coupon (case insensitive)
                        coupon_input = driver.find_element(By.XPATH, "//input[contains(translate(@name, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'coupon') or contains(translate(@id, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'coupon')]")
                    except:
                        try:
                            # Tìm tất cả input và thử input thứ 3 (sau name và email)
                            all_inputs = driver.find_elements(By.TAG_NAME, "input")
                            print(f"Tìm thấy {len(all_inputs)} input fields")
                            # In ra để debug
                            for i, inp in enumerate(all_inputs):
                                try:
                                    print(f"  Input {i+1}: type={inp.get_attribute('type')}, name={inp.get_attribute('name')}, id={inp.get_attribute('id')}, placeholder={inp.get_attribute('placeholder')}")
                                except:
                                    pass
                            # Thử input thứ 3 hoặc input text cuối cùng
                            if len(all_inputs) >= 3:
                                coupon_input = all_inputs[2]  # Input thứ 3 (index 2)
                            elif len(all_inputs) > 0:
                                # Tìm input text cuối cùng (không phải submit)
                                for inp in reversed(all_inputs):
                                    if inp.get_attribute('type') in ['text', None, '']:
                                        coupon_input = inp
                                        break
                        except Exception as e:
                            print(f"Không tìm thấy trường coupon: {e}")
        
        if coupon_input:
            coupon_input.clear()
            coupon_input.send_keys(coupon)
            print("✓ Đã nhập coupon")
            if not fast_mode:
                time.sleep(1)
            
            # Tìm và click nút Apply để áp dụng coupon
            print("Đang tìm nút Apply...")
            apply_button = None
            try:
                # Thử tìm button có text "Apply"
                apply_button = wait.until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Apply') or contains(text(), 'apply') or contains(text(), 'Áp dụng') or contains(text(), 'ÁP DỤNG')]"))
                )
            except:
                try:
                    # Thử tìm button gần coupon input
                    apply_button = driver.find_element(By.XPATH, "//button[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'apply')]")
                except:
                    try:
                        # Tìm button sau coupon input
                        all_buttons = driver.find_elements(By.TAG_NAME, "button")
                        print(f"Tìm thấy {len(all_buttons)} button(s)")
                        # Tìm button gần nhất sau coupon input
                        for btn in all_buttons:
                            btn_text = btn.text.lower()
                            if 'apply' in btn_text or 'áp dụng' in btn_text:
                                apply_button = btn
                                break
                    except:
                        pass
            
            if apply_button:
                # Scroll đến button
                driver.execute_script("arguments[0].scrollIntoView(true);", apply_button)
                if not fast_mode:
                    time.sleep(0.5)
                
                # Click nút Apply
                try:
                    apply_button.click()
                    print("✓ Đã click vào nút Apply")
                except:
                    try:
                        driver.execute_script("arguments[0].click();", apply_button)
                        print("✓ Đã click vào nút Apply (bằng JavaScript)")
                    except Exception as e:
                        print(f"⚠ Không thể click nút Apply: {e}")
                
                # Chờ coupon được áp dụng (sử dụng explicit wait nếu có thể)
                if fast_mode:
                    time.sleep(0.5)  # Giảm thời gian chờ
                else:
                    time.sleep(2)
            else:
                print("⚠ Không tìm thấy nút Apply, tiếp tục...")
        else:
            print("⚠ Không tìm thấy trường coupon, bỏ qua...")
        
        # Tìm và click nút "Complete my purchase"
        print("Đang tìm nút Complete my purchase...")
        complete_button = None
        try:
            # Thử tìm button có text "Complete my purchase"
            complete_button = wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Complete my purchase') or contains(text(), 'complete my purchase') or contains(text(), 'Complete My Purchase')]"))
            )
        except:
            try:
                # Thử tìm bằng partial text
                complete_button = wait.until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'complete')]"))
                )
            except:
                try:
                    # Tìm button có chứa "purchase"
                    complete_button = driver.find_element(By.XPATH, "//button[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'purchase')]")
                except:
                    try:
                        # Tìm tất cả button và chọn button lớn/cuối cùng
                        all_buttons = driver.find_elements(By.TAG_NAME, "button")
                        print(f"Tìm thấy {len(all_buttons)} button(s)")
                        # Tìm button có text dài nhất (thường là nút chính)
                        if len(all_buttons) > 0:
                            complete_button = max(all_buttons, key=lambda b: len(b.text) if b.text else 0)
                    except:
                        pass
        
        if complete_button:
            # Scroll đến button
            driver.execute_script("arguments[0].scrollIntoView(true);", complete_button)
            if not fast_mode:
                time.sleep(0.5)
            
            # Click nút Complete my purchase
            try:
                complete_button.click()
                print("✓ Đã click vào nút Complete my purchase")
            except:
                try:
                    driver.execute_script("arguments[0].click();", complete_button)
                    print("✓ Đã click vào nút Complete my purchase (bằng JavaScript)")
                except Exception as e:
                    print(f"⚠ Không thể click nút Complete my purchase: {e}")
        else:
            print("⚠ Không tìm thấy nút Complete my purchase")
        
        # Chờ phản hồi
        print("Đang chờ phản hồi từ trang web...")
        if fast_mode:
            time.sleep(2)  # Giảm thời gian chờ
        else:
            time.sleep(5)
        
        # Kiểm tra kết quả
        current_url = driver.current_url
        page_source = driver.page_source.lower()
        
        status = "unknown"
        if "success" in page_source or "thành công" in page_source or "đăng ký thành công" in page_source:
            print("\n✓ Đăng ký thành công!")
            status = "success"
        elif "error" in page_source or "lỗi" in page_source or "thất bại" in page_source:
            print("\n✗ Có lỗi xảy ra trong quá trình đăng ký")
            status = "error"
        else:
            print("\n? Không thể xác định kết quả, vui lòng kiểm tra thủ công")
            status = "unknown"
        
        print(f"\nThông tin đã sử dụng:")
        print(f"  - Tên: {name}")
        print(f"  - Email: {email}")
        print(f"  - Coupon: {coupon}")
        
        # Lưu thông tin đăng ký
        save_registration_info(name, email, coupon, status)
        
        # Giữ trình duyệt mở thêm để xem kết quả
        if not fast_mode:
            print("\nGiữ trình duyệt mở thêm 5 giây để xem kết quả...")
            time.sleep(5)
        
    except Exception as e:
        print(f"\n✗ Lỗi: {str(e)}")
        print("\nĐang chụp màn hình để debug...")
        try:
            driver.save_screenshot("error_screenshot.png")
            print("Đã lưu screenshot vào error_screenshot.png")
        except:
            pass
        
    finally:
        print("\nĐang đóng trình duyệt...")
        driver.quit()
        print("Hoàn tất!")

if __name__ == "__main__":
    # Đọc config và chạy
    config = load_config()
    register_account(
        name=config.get("name"),  # Để None để tự động tạo, hoặc nhập tên cụ thể
        email=config.get("email"),  # Để None để tự động tạo, hoặc nhập email cụ thể
        coupon=config.get("coupon", "damuatdh"),  # Mã coupon mặc định
        fast_mode=config.get("fast_mode", True)  # Chế độ nhanh
    )

