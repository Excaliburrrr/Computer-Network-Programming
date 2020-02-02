import multiprocessing
import os


def copy_file(old_folder_name, file_name, new_folder_name, q):
	with open(old_folder_name + "/" + file_name, 'rb') as f:
		content = f.read()

	with open(new_folder_name + "/" + file_name, 'wb') as f:
		f.write(content)
	
	q.put(file_name)



def main():
	old_folder_name = input("请输入想要复制的文件：")
	files = os.listdir(old_folder_name)
	new_folder_name = input("请输入目标地址：")
	new_folder_name = new_folder_name + "/" + os.path.basename(old_folder_name) + "[复制]"
	try:
		os.mkdir(new_folder_name)
	except:
		print("文件已存在.")
		pass
	# 创建进程池
	po = multiprocessing.Pool(5)
	q = multiprocessing.Manager().Queue()
	for file in files:
		po.apply_async(copy_file, (old_folder_name, file, new_folder_name, q))
	
	finished_num = 0	
	all_file_num = len(files)
	while True:
		finished_file = q.get()
		finished_num += 1
		print("\r完成的进度：%.2f%%" %(finished_num * 100 / all_file_num), end="")
		if finished_num >= all_file_num:
			print()
			break
			

	po.close()
	po.join()


if __name__ == '__main__':
	main()
