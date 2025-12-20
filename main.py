import os
import time
import copy
import sys
import webbrowser as wb
sys.stdout.reconfigure(encoding="utf-8")
from customs import show
from global_constants import COLORS_FILE, SETTINGS_FILE, HISTORY_FILE
from file_handlers import read_text, update_data, read_json
from general import logo as L, Generator, get_numeric_post_id
from security import security as S
from updater import updates
from core.cli import CLI
# from core import batch_runner
# from queue import Queue
ALL_THEADS = []
history = read_json(HISTORY_FILE)
# result_container = Queue() # list like structure and by default its thread safe and provides put, get like mutable methods 
result_container = {
    "success":[],   # id_no: name, .....
    "faliure":[],   # id_no: name, .....
    "locked":[]     # "cookie", "cookie"....
}

time.sleep(2)
class comenter:
    def __init__(self, result_container, ALL_THEADS):
        self.result_container = result_container
        self.logo_length = None
        self.cookies = history["cookies"]
        self.comment = history["comment"]
        self.post_link = history["post_link"]
        self.total_comments_to_do = history["total_comments_to_do"]
        self.threads_count = history["threads_count"]
        self.locked_till_now = history["locked_till_now"]
        self.sucess_till_now = history["sucess_till_now"]
        self.options = {"from_page": True,"from_user": True}
        self.ALL_THEADS = ALL_THEADS
        self.reserve_cookies = []
        self.is_first=False

    def start(self):
        # S(REQUITRTEMENTS_FILE).check()
        # updates().check()
        self.clear()
        self.ask_all_data()
        self.clear()
        self.logo_length = L(COLORS_FILE, SETTINGS_FILE).print_logo()
        # # self.show_info("nj")
        # choice = self.get_choice("Choice", "int")
        # if choice in [0,1,2,3,4,5,6]:self.run_choice(choice) 
        # else:
        #     show(f"invalid option {choice} ")
        #     time.sleep(3)
        #     return self.start()
        self.start_thread()

    def run_choice(self, choice: int):
        # if choice in [1, 2, 3]:self.ask_all_data(choice)
        if choice in [1, 2, 3]:self.start_thread()
        elif choice == 4:wb.open("https://github.com/offiicialkamal/Facebook-Automation-2.0/blob/main/readme.md")
        elif choice == 5:wb.open("https://github.com/offiicialkamal/Facebook-Automation-2.0.git")
        elif choice == 6:pass
        elif choice == 0:sys.exit()
        else:wb.open("https://github.com/offiicialkamal")

    # def ask_all_data(self, choice):
    def ask_all_data(self):
        comment = ""
        self.set_cookie()
        # self.set_post_link()
        self.set_total_comments_to_do()
        self.set_threads_count()
        self.set_comment()
        # self.print_line()
        if not (self.cookies, self.post_link, self.total_comments_to_do, self.threads_count, self.set_comment):
            show("Some Required data is missingg Please reStart the tool and enter the all details properly")
        

    # def get_cookie_new(self, path):
    #     for cookie in read_text(path).splitlines():
    #         self.cookies.append(cookie)

    def get_choice(self, subject: str, t=""):
        if not t:
            choice = input(subject) if (" " in subject) else input(f"Enter Your {subject} : ")
            if not choice:return
        else:
            try:
                choice = int(input(subject) if (" " in subject) else input(f"Enter Your {subject} : "))
            except Exception:
                show("Invalid 1input")
                return self.get_choice(subject, t)
        return choice

    def clear(self):
         os.system('cls' if os.name == 'nt' else 'clear')

    def print_line(self):
        length = self.logo_length
        # print("<< " + "━" * length + " >>")
        print("━" * length)
    
    
    is_first=False
    def show_info(self, data, completed=False):
        # print(data)
        # return 
        # data = {
        #     "total_profiles": self.ready_sessions,
        #     "total_ids": self.total_profiles,
        #     "loaded_pages": self.total_profiles - self.total_profiles,
        #     "locked_ids": self.locked_ids
        # }
        if self.is_first:
            print("\033[11A", end="")
        self.is_first = True

        l = self.logo_length
        print("\033[104m" + f"{'LOADED DATA' if completed else 'LOADING PLEASE WAIT'}".center(l) + "\033[49m")
        self.print_line()
        l+=(-8)
        l+=(-8)
        print()
        print("\tLOADED SPEED               ".ljust(l//2)  + f"{self.threads_count}/Sec\t".rjust(l//2))
        print("\tTOTAL CMTs                ".ljust(l//2)  + f"{self.total_comments_to_do}/ACC\t".rjust(l//2))
        print("\tOVERALL IDs                ".ljust(l//2)  + f"{len(self.cookies)+len(self.locked_till_now)} IDs\t".rjust(l//2))
        print("\tTOTAL LOADED IDS      ".ljust(l//2)  + f"{data.get('total_ids')} IDs\t".rjust(l//2))
        print("\tTOTAL LOADED PAGES      ".ljust(l//2)  + f"{data.get('total_ids')-data.get('total_profiles')} IDs\t".rjust(l//2))
        print("\tTOTAL LOADED PROFILES      ".ljust(l//2)  + f"{data.get('total_profiles')} IDs\t".rjust(l//2))
        print("\tTOTAL LOCKED TILL NOW      ".ljust(l//2)  + f"{len(self.locked_till_now) + data['locked_ids'] or 0} IDs\t".rjust(l//2))

        self.print_line()
        
    def show_options(self):
        try:
            print("   01 FROM PAGE")
            print("   02 FROM PROFILE")
            print("   03 FROM PAGE + PROFILE")
            print("   04 DOCUMENTATION")
            print("   05 SEE SOURCE CODE")
            print("   06 SETTINGS")
            print("   00 Exit")
            self.print_line()
        except Exception as e:
            print("Unexpected Input Please choose one of the given option",  e)
            time.sleep(3)
            self.start()
    def show_results(self):
        self.print_line()
        self.print_line()
        total_locked_ids = len(self.result_container['locked'])
        total_ids_with_coment_block = len(self.result_container['faliure'])
        total_comments_sent = len(self.result_container['success'])
        print(f'\033[42mTOTAL COMMENTS DONE {total_comments_sent}\033[49m')
        print(f'\033[100mTOTAL COMMENTS FAILD {total_ids_with_coment_block}\033[49m')
        print(f'\033[101mTOTAL LOCKED IDS {total_locked_ids}\033[49m')


    ###########################################################################
    ######################       small methods      ###########################

    def set_cookie(self):
        path = self.get_choice("cookie file path: ")
        if not path: return
        try:
            cookies = []
            new_cookie = read_text(path)
            # print(type(new_cookie))
            for cookie in new_cookie.splitlines():
                # user_agent = Generator().generate()
                # cookies.append({cookie: [user_agent]})
                cookies.append(cookie)
            self.cookies = cookies
            update_data(HISTORY_FILE, "cookies", cookies)
        except Exception as e:
            show("File Not Found Retry")
            print(e)
            return self.set_cookie()
    def set_post_link(self):
        link = self.get_choice("post_link: ")
        if not link: return
        p_id = get_numeric_post_id(link)
        if not p_id: print("invalid post id retry boss");return self.set_post_link()
        self.post_link = p_id
        update_data(HISTORY_FILE, "post_link", p_id)
    def set_total_comments_to_do(self):
        number_of_coments = input("Total Comments : ")
        if not number_of_coments: return
        try:self.total_comments_to_do = int(number_of_coments)
        except:print("invalid input");self.set_total_comments_to_do()
        update_data(HISTORY_FILE, "total_comments_to_do", int(number_of_coments))
    def set_threads_count(self):
        threads_count = input("Enter Speed (1 - 10 recomended): ")
        if not threads_count: return
        try:self.threads_count = int(threads_count)
        except: print("invalid input");self.set_threads_count()
        update_data(HISTORY_FILE, "threads_count", int(threads_count))
    def set_comment(self):
        is_enterd= False
        comment = ""
        while True:
            cmt = input("Comment: ")
            if not cmt:break
            is_enterd = True
            comment += "\n" + cmt
        if not is_enterd: return
        self.comment = comment
        update_data(HISTORY_FILE, "comment", comment)
    def start_thread(self):
        # print("started")
        ## pass the alll data hear we have original work
        data = [self.post_link, self.comment, self.total_comments_to_do, self.threads_count]
        functions = [self.set_post_link, self.show_options]
        cli = CLI(self.show_info, self.logo_length, self.cookies, data, functions, )
        cli.run()
        
comenter(result_container, ALL_THEADS).start()
