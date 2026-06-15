import logging

logging.basicConfig(
    filename = "check.log",
    filemode = "a",
    level = logging.DEBUG,
    format = '%(asctime)s - %(levelname)s - %(message)s'
)


# cn1
def show_devices(devices):
    logging.info("Nguoi dung yeu cau xem danh sach thiet bi.")

    if len(devices) == 0:
        logging.warning("Danh sach thiet bi dang trong, khong co du lieu de hien thi.")
        print("He thong hien chua co thiet bi giam sat nao!")
        return
 
    print("--- Danh Sách Thiết Bị Giám Sát ---")
    print(f"{'MA TB':<8} | {'VI TRI PHAN XUONG':<22} | {'CHI SO CU':>10} | {'CHI SO MOI':>10} | {'TRANG THAI'}")
    print("-" * 70)
 
    for item in devices:
        print(f"{item['id']:<8} | {item['location']:<22} | {item['old_index']:>10} | {item['new_index']:>10} | {item['status']}")

    logging.info(f"Hien thi thanh cong {len(devices)} thiet bi.")


# Chức năng 2
def update_indices(devices):
    device_id = input("Nhập mã thiết bị: ").strip()
    device = None
    for item in devices:
        if item["id"] == device_id:
            device = item
            break
    if device is None:
        print("[ERR-E01] Không tìm thấy mã thiết bị trong hệ thống!")
        logging.error(f"Không tìm thấy thiết bị có mã {device_id}")
        return
    while True:
        try:
            old_index = int(input("Nhập chỉ số cũ: "))
            if old_index < 0:
                print("[LỖI] Chỉ số phải lớn hơn hoặc bằng 0!")
                continue
            break
        except ValueError:
            print("[LỖI] Vui lòng nhập số hợp lệ!")
    while True:
        try:
            new_index = int(input("Nhập chỉ số mới: "))
            if new_index < 0:
                print("[LỖI] Chỉ số phải lớn hơn hoặc bằng 0!")
                continue
            if new_index < old_index:
                print("[ERR-E02] Chỉ số mới không được nhỏ hơn chỉ số cũ!")
                continue
            break
        except ValueError:
            print("[LỖI] Vui lòng nhập số hợp lệ!")
    device["old_index"] = old_index
    device["new_index"] = new_index
    print(f"Đã cập nhật chỉ số cho thiết bị {device_id} thành công!")

    logging.info(
        f"Cập nhật thiết bị {device_id} | "
        f"Old Index: {old_index} | "
        f"New Index: {new_index}"
    )

def activate_overload_warning(devices: list) -> None:
    """
    Nhập mã thiết bị từ bàn phím để duyệt cảnh báo quá tải.
    - Không tìm thấy mã thiết bị -> Báo lỗi ERR-E01
    - Đã ở trạng thái Overload từ trước -> Báo lỗi ERR-E04
    - Tiêu thụ > 5,000 kWh -> Chuyển sang Overload & Log WARNING
    - Tiêu thụ <= 5,000 kWh -> Không đủ điều kiện kích hoạt
    """
    print("\n--- KÍCH HOẠT TRẠNG THÁI CẢNH BÁO QUÁ TẢI ---")
    device_id = input("Nhập mã thiết bị cần duyệt cảnh báo: ").strip()
    
    # Tìm kiếm thiết bị trong danh sách
    target_device = None
    for device in devices:
        if device['id'] == device_id:
            target_device = device
            break
            
    # Trường hợp không tìm thấy mã thiết bị
    if not target_device:
        print(f"[ERR-E01] Mã thiết bị '{device_id}' không tồn tại trên hệ thống!")
        return

    # Trường hợp thiết bị tìm thấy đã ở trạng thái Overload từ trước
    if target_device['status'] == 'Overload':
        print(f"[ERR-E04] Thiết bị '{device_id}' đã ở trạng thái Overload từ trước.")
        return

    # Tính toán lượng điện tiêu thụ thực tế
    consumption = target_device['new_index'] - target_device['old_index']
    print(f"Lượng điện tiêu thụ thực tế của thiết bị {device_id}: {consumption:,} kWh")

    # Kiểm tra điều kiện vượt mức 5,000 kWh
    if consumption > 5000:
        target_device['status'] = 'Overload'
        print("=> Kết quả duyệt: ĐỦ ĐIỀU KIỆN KÍCH HOẠT")
        
        # Phát ra thông báo log mức WARNING theo đúng yêu cầu
        logging.warning(
            f"Thiết bị {device_id} tại {target_device['location']} tiêu thụ {consumption:,} kWh -> Đã kích hoạt trạng thái Overload!"
        )
    else:
        print("=> Kết quả duyệt: Không đủ điều kiện kích hoạt (Tiêu thụ chưa vượt quá 5,000 kWh).")

# chức năng 4
def calculate_energy_financials(devices):
    logging.debug(f"Calculating energy financials for {len(devices)} devices.")

    if (not devices):
        return (0.0, 0.0, 0.0)

    total_kwh = 0

    for item in devices:
        total_kwh += (item["new_index"] - item["old_index"])

    base_cost = total_kwh * 3000
    discount_percent = 0

    if total_kwh >= 50000:
        discount_percent = 3

    final_cost = base_cost * (1 - discount_percent / 100)
    return (total_kwh, discount_percent, final_cost)

def show_menu():
    print("\n" + "="*50)
    print("      SMART ENERGY MONITOR - PHÒNG CƠ ĐIỆN      ")
    print("="*50)
    print("1. Xem danh sách thiết bị giám sát")
    print("2. Cập nhật chỉ số điện tiêu thụ (Check-in)")
    print("3. Kích hoạt trạng thái cảnh báo quá tải")
    print("4. Tính tổng lượng điện & Chi phí năng lượng")
    print("5. Thoát chương trình")
    print("="*50)

def main():
    devices = [
        {'id': 'M01', 'location': 'Mechanical Shop A', 'old_index': 1200, 'new_index': 4500, 'status': 'Normal'},
        {'id': 'M02', 'location': 'Assembly Line B', 'old_index': 2300, 'new_index': 8500, 'status': 'Overload'}
    ]
    
    while True:
        show_menu()
        
        try:
            choice = int(input("Mời chọn chức năng (1-5): "))
        except ValueError:
            print("[LỖI] Vui lòng chỉ nhập số nguyên từ 1 đến 5!")
            continue
            
        if choice == 1:
            print("\n--> Bạn đã chọn Chức năng 1: Xem danh sách thiết bị.")
            show_devices(devices)
            
        elif choice == 2:
            update_indices(devices)
            
        elif choice == 3:
            print("\n--> Bạn đã chọn Chức năng 3: Kích hoạt trạng thái cảnh báo quá tải.")
            activate_overload_warning(devices)
            
        elif choice == 4:
            total_kwh, discount_percent, final_cost = (calculate_energy_financials(devices))

            print("\n===== BÁO CÁO NĂNG LƯỢNG =====")
            print(f"Tổng điện tiêu thụ : {total_kwh:,.0f} kWh")
            print(f"Chiết khấu áp dụng : {discount_percent}%")
            print(f"Tổng tiền thanh toán: {final_cost:,.0f} VND")
            
        elif choice == 5:
            print("\nCảm ơn bạn đã sử dụng hệ thống. Tạm biệt!")
            break
            
        else:
            print("[LỖI] Lựa chọn không hợp lệ! Vui lòng chọn lại từ 1 đến 5.")

main()
