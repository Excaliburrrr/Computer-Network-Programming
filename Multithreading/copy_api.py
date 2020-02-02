import multiprocessing
import os


def copy_file(old_folder_name, file_name, new_folder_name):
    with open(old_folder_name + "/" + file_name, 'rb') as f:
        content = f.read()

    with open(new_folder_name + "/" + file_name, 'wb') as f:
        f.write(content)


def main():
    old_folder_name = input("请输入想要复制的文件：")
    files = os.listdir(old_folder_name)
    new_folder_name = input("请输入目标地址：")
    try:
        os.mkdir(new_folder_name + "/" + os.path.basename(old_folder_name) + "[复制]")
    except:
        print("文件已存在.")
        pass
    # 创建进程池
    po = multiprocessing.Pool(5)

    for file in files:
        po.apply_async(copy_file, (old_folder_name, file, new_folder_name))

    po.close()
    po.join()


if __name__ == '__main__':
    main()