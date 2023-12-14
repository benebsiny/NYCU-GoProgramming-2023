
import difflib
import os
import sys

testcase = [
    (
        ["go", "run", "lab09.go"],
        "1. 名字：Ommmmmm5566，留言: 哈哈哈哈哈ㄏㄏㄏㄏ哈哈哈哈哈哈，時間： 12/09 03:18\n"+\
        "2. 名字：Ommmmmm5566，留言: 笑死，時間： 12/09 03:18\n"+\
        "3. 名字：husky01，留言: 樓上…，時間： 12/09 03:27\n"+\
        "4. 名字：bakapika，留言: ㄏㄏ，時間： 12/09 06:25\n"+\
        "5. 名字：scmdwyam，留言: XDD，時間： 12/09 08:48\n"+\
        "6. 名字：L2e2o4，留言: ㄏㄏ，時間： 12/09 09:21\n"+\
        "7. 名字：NobleDino，留言: ㄏㄏ，時間： 12/09 09:34\n"+\
        "8. 名字：tottoko0908，留言: ㄏㄏ，時間： 12/09 09:45\n"+\
        "9. 名字：lmh911152，留言: ㄏㄏ，時間： 12/09 09:56\n"+\
        "10. 名字：monicamomo，留言: ㄏㄏ，時間： 12/09 10:25\n",
        False
    ),
    (
        ["go", "run", "lab09.go", "-max", "5"],
        "1. 名字：Ommmmmm5566，留言: 哈哈哈哈哈ㄏㄏㄏㄏ哈哈哈哈哈哈，時間： 12/09 03:18\n"+\
        "2. 名字：Ommmmmm5566，留言: 笑死，時間： 12/09 03:18\n"+\
        "3. 名字：husky01，留言: 樓上…，時間： 12/09 03:27\n"+\
        "4. 名字：bakapika，留言: ㄏㄏ，時間： 12/09 06:25\n"+\
        "5. 名字：scmdwyam，留言: XDD，時間： 12/09 08:48\n",
        False
    ),
    (
        ["go", "run", "lab09.go", "-hello"],
        "flag provided but not defined: -hello\n"+\
        "Usage of\n"+\
        "  -max int\n"+\
    	"    	Max number of comments to show (default 10)\n"+\
        "exit status 2\n",
        True
    ),
    (
        ["go", "run", "lab09.go", "-max"],
        "flag needs an argument: -max\n"+\
        "Usage of\n"+\
        "  -max int\n"+\
    	"    	Max number of comments to show (default 10)\n"+\
        "exit status 2\n",
        True
    ),
    (
        ["go", "run", "lab09.go", "-max", "hello"],
        'invalid value "hello" for flag -max: parse error\n'+\
        "Usage of\n"+\
        "  -max int\n"+\
    	"    	Max number of comments to show (default 10)\n"+\
        "exit status 2\n",
        True
    )
]

def edits_string(first, second):

        first = first.splitlines(1)
        second = second.splitlines(1)
        result = difflib.unified_diff(first, second)

        colored_diff = []
        for line in result:
            if line.startswith(' '):
                colored_diff.append('\033[0m' + line)
            elif line.startswith('+'):
                colored_diff.append('\033[32m' + line)
            elif line.startswith('-'):
                colored_diff.append('\033[31m' + line)
        return ''.join(colored_diff) + '\033[0m'

def main():
    try:
        for i, (args, ans, isError) in enumerate(testcase):
            os.system(f"{' '.join(args)} > result_{i}.txt 2>&1")
            with open(f"result_{i}.txt", "r", encoding='utf-8') as file_:
                output = file_.read()
                if isError:
                    uidx = output.find("Usage of")
                    if uidx == -1:
                        print(f"\033[1;31m[ERROR]\033[0;33m\nCommand:\033[0m\n{' '.join(args)}\n\033[0;33mResult:\033[0m")
                        print(edits_string(ans, output))
                        break
                    tidx = output.index("\n", uidx)
                    if tidx == -1:
                        print(f"\033[1;31m[ERROR]\033[0;33m\nCommand:\033[0m\n{' '.join(args)}\n\033[0;33mResult:\033[0m")
                        print(edits_string(ans, output))
                        break
                    output = output[:uidx + 8] + output[tidx:]

                if output != ans:
                    print(f"\033[1;31m[ERROR]\033[0;33m\nCommand:\033[0m\n{' '.join(args)}\n\033[0;33mResult:\033[0m")
                    print(edits_string(ans, output))
                    break
        else:
            return 0
    finally:
        for i in range(len(testcase)):
            if os.path.exists(f"result_{i}.txt"):
                os.remove(f"result_{i}.txt")
    return 1

if __name__ == "__main__":
    status = main()
    if status == 0:
        print("\033[1;32mPASS\033[0m")
    sys.exit(status)
