detective = {}
evidences = {}
id_list = []
linelist = []
data = open("crime_scene.txt", "r")
for line in data:
    if len(line.split()) > 0:
        linelist.append(line)
data.close()


def evidence(lst, n):
    a = lst[n].split()
    if n == 0 and len(a) > 0:
        detective["W"] = a[0]
        detective["T"] = a[1]
        return
    if n == 1 and len(a) > 0:
        detective["N"] = a[0]
    if n > 1 and len(a) > 0:
        id_list.append(a[0])
        evidences[a[0]] = {"W": a[1], "T": a[2], "V": a[3]}
    evidence(lst, n - 1)


evidence(linelist, len(linelist) - 1)
combs_time = {}
combs_weight = {}
combs_both = {}


def sort_lst(lst, lenn, x=0, check=0):
    if x == lenn:
        if check == lenn:
            return
        sort_lst(lst, lenn, check + 1, check + 1)
        return
    elif lst[check] > lst[x]:
        lst[check], lst[x] = lst[x], lst[check]
    sort_lst(lst, lenn, x + 1, check)


def weight_checker(weight, evidence_lst, lenn, w=0):
    if w > weight:
        return False
    if lenn == 0:
        return True
    w += int(evidences[str(evidence_lst[lenn - 1])]["W"])
    return weight_checker(weight, evidence_lst, lenn - 1, w)


def time_checker(time, evidence_lst, lenn, t=0):
    if t > time:
        return False
    if lenn == 0:
        return True
    t += int(evidences[str(evidence_lst[lenn - 1])]["T"])
    return time_checker(time, evidence_lst, lenn - 1, t)


def max_value(n, evidence_lst, v=0, lenn=0):
    if n == 0:
        new = evidence_lst.copy()
        sort_lst(new, lenn)
        if weight_checker(int(detective["W"]), new, lenn, 0):
            combs_weight[v] = new
        if time_checker(int(detective["T"]), new, lenn, 0):
            combs_time[v] = new
        if weight_checker(int(detective["W"]), new, lenn, 0) and time_checker(int(detective["T"]), new, lenn, 0):
            combs_both[v] = new
        return
    v += int(evidences[id_list[n - 1]]["V"])
    evidence_lst.append(int(id_list[n - 1]))
    lenn += 1
    max_value(n - 1, evidence_lst, v, lenn)
    v = v - int(evidences[id_list[n - 1]]["V"])
    evidence_lst.pop()
    lenn -= 1
    max_value(n - 1, evidence_lst, v, lenn)


max_value(int(detective["N"]), [])


def lsttostr(lst):
    if len(lst) == 0:
        return ""
    return (str(lst[0]) + " " + lsttostr(lst[1:])).rstrip()


def maxv(lst, m=0):
    if len(lst) == 0:
        return m
    if lst[0] > m:
        return maxv(lst[1:], lst[0])
    else:
        return maxv(lst[1:], m)


mw = maxv(list(combs_weight.keys()))
mt = maxv(list(combs_time.keys()))
mb = maxv(list(combs_both.keys()))
part_1 = open("solution_part1.txt", "w")
part_1.write(str(mw) + "\n" + lsttostr(combs_weight[mw]))
part_1.close()
part_2 = open("solution_part2.txt", "w")
part_2.write(str(mt) + "\n" + lsttostr(combs_time[mt]))
part_2.close()
part_3 = open("solution_part3.txt", "w")
part_3.write(str(mb) + "\n" + lsttostr(combs_both[mb]))
part_3.close()
