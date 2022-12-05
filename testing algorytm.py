current_group_user_list = {
    id: '1',
    id: '2',
    id: '3',
    id: '4',
    id: '10',
    id: '12'
}
weeks = {}
ready_selected = 0

for i in range(54):
    for j in range(5):
        if j == ready_selected:
            if j==4:
                weeks.wor_leader = current_group_user_list[j+1]
                weeks.wor_engager = current_group_user_list[1]
                ready_selected =  j
            else:
                weeks.wor_leader = current_group_user_list[j+1]
                weeks.wor_engager = current_group_user_list[j+2]
                ready_selected =  j
print (weeks)
