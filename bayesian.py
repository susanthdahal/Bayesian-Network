import sys,itertools

class Bayes:
    def __init__(self):
        self.query=[]
        self.dict={}
        self.parents={}
        self.nodes=[]

    def read_file(self,file):
        text=file.read().split('\n')
        self.make_network(text)

    def make_network(self,text):
        all_lines=[]
        one_set=[]
        for line in text:
            if line=='':
                break
            if line[0]=='*':
                all_lines.append(one_set)
                one_set=[]
            else:
                one_set.append(line)
        all_lines.append(one_set)
        self.query=all_lines[0]
        for i in range(1,len(all_lines)):
            node=all_lines[i][0].split(' | ')
            self.nodes.append(node[0])
            self.parents[node[0]]=[]
            if len(node)>1:
                parents=node[1].split(' ')
                if '' in parents:
                    parents.remove('')
                for p in parents:
                    self.parents[node[0]].append(p)
                for j in range(1,len(all_lines[i])):
                    if all_lines[i][j]=='decision':
                        possitive_prob=1.0
                        negative_prob=1.0
                    else:
                        values=all_lines[i][j].split(' ')
                        possitive_prob=float(values[0])
                        negative_prob=1-possitive_prob
                    pos_string=node[0]+' = +'
                    neg_string=node[0]+' = -'
                    parent_string=""
                    for k  in range(len(self.parents[node[0]])):
                        if k==0:
                            parent_string+=self.parents[node[0]][k]+' = '+values[k+1]
                        else:
                            parent_string+=', '+self.parents[node[0]][k]+' = '+values[k+1]
                    if pos_string not in self.dict:
                        self.dict[pos_string]={}
                        self.dict[neg_string]={}
                    self.dict[pos_string][parent_string]=possitive_prob
                    self.dict[neg_string][parent_string]=negative_prob
            else:
                for j in range(1,len(all_lines[i])):
                    if all_lines[i][j]=='decision':
                        possitive_prob=1.0
                        negative_prob=1.0
                    else:
                        values=all_lines[i][j].split(' ')
                        possitive_prob=float(values[0])
                        negative_prob=1-possitive_prob
                    pos_string=node[0]+' = +'
                    neg_string=node[0]+' = -'
                    parent_string="None"
                    if pos_string not in self.dict:
                        self.dict[pos_string]={}
                        self.dict[neg_string]={}
                    self.dict[pos_string][parent_string]=possitive_prob
                    self.dict[neg_string][parent_string]=negative_prob
        if 'utility' in self.nodes:
            self.nodes.remove('utility')
    def display(self):
        print self.dict
        print self.nodes
        print(self.parents)

    def calculate_expected(self,my_string):
        conditional_prob=my_string.split(' | ')
        if len(conditional_prob)>1:
            joint_prob1=conditional_prob[0]+', '+conditional_prob[1]
        else:
            joint_prob1=my_string

        flag=False
        for p in self.parents['utility']:
            if p in joint_prob1:
                flag=True
                break
        expected_utility=[]
        for keys in self.dict['utility = +']:
            temp=joint_prob1.split(',')
            flag2=False
            for node in temp:
                if node in keys and flag==True:
                    flag2=True
            if flag2==False and flag==True:
                continue
            temp=joint_prob1
            temp+=', '+keys
            prob1=self.calc(str(temp))
            if len(conditional_prob)>1:
                prob2=self.calc(joint_prob1)
                util=prob1/prob2
                util*=float(self.dict['utility = +'][keys])
                expected_utility.append(util)
                continue
            util=prob1
            util*=float(self.dict['utility = +'][keys])
            expected_utility.append(util)
        return "%0.0f"%((sum(expected_utility)))



    def findProbability(self):
        question=self.query
        for i in range(len(question)):
            if(question[i][0]=='P'):
                my_string=str(question[i][2:-1])
                conditional_prob=my_string.split(' | ')
                if len(conditional_prob)>1:
                    joint_prob1=conditional_prob[0]+', '+conditional_prob[1]
                    joint_prob2=conditional_prob[1]
                    joint_prob1=self.calc(str(joint_prob1))
                    joint_prob2=self.calc(str(joint_prob2))
                    print "%0.2f"%(joint_prob1/joint_prob2)

                else:
                    print "%0.2f"%(self.calc(str(my_string)))
            elif question[i][0]=='E':
                my_string=str(question[i][3:-1])
                print self.calculate_expected(my_string)
            else:
                my_string=str(question[i][4:-1])
                conditional_prob=my_string.split(' | ')
                if len(conditional_prob)>1:
                    nodes=conditional_prob[0].split(', ')
                else:
                    nodes=my_string.split(', ')
                my_list=list(itertools.product(['+','-'], repeat=len(nodes)))
                probability_list=[]
                for i in range(len(my_list)):
                    my_string=''
                    for j in range(len(my_list[i])):
                        if my_string=='':
                            my_string+=nodes[j]+' = '+my_list[i][j]
                        else:
                            my_string+=', '+nodes[j]+' = '+my_list[i][j]
                    if len(conditional_prob)>1:
                        my_string+=' | '+conditional_prob[1]
                    probability_list.append(int(self.calculate_expected(my_string)))

                max_value=max(probability_list)
                index_pos=probability_list.index(max_value)
                for j in range(len(nodes)):
                    print my_list[index_pos][j],
                print(str(max_value))




    def calc(self,my_string):
        my_string=my_string.split(', ')
        given_nodes=[]
        valueof_nodes=[]
        for i in range(len(my_string)):
            temp=my_string[i].split(' ')
            given_nodes.append(temp[0])
            valueof_nodes.append(temp[-1])

        table=list(itertools.product(['+','-'], repeat=len(self.nodes)))
        node_index={}
        for i in range(len(self.nodes)):
            node_index[self.nodes[i]]=i
            if self.nodes[i] in given_nodes:
                node_val=valueof_nodes[given_nodes.index(self.nodes[i])]
                temp=[]
                for j in range(len(table)):
                    if table[j][i]!=node_val:
                        temp.append(j)
                new_table=[]
                for j in range(len(table)):
                    if j not in temp:
                        new_table.append(table[j])
                table=new_table
        probability_list=[]
        for i in range(len(table)):
            prod=1.0
            for j in range(len(self.nodes)):
                outer_key=self.nodes[j]+' = '+table[i][j]
                inner_key="None"
                for k in self.parents[self.nodes[j]]:
                    if inner_key=="None":
                        inner_key=k+' = '+table[i][node_index[k]]
                    else:
                        inner_key+=', '+k+' = '+table[i][node_index[k]]
                prod*=self.dict[outer_key][inner_key]
            probability_list.append(prod)
        return sum(probability_list)


file=open("sample11.txt",'r')
obj=Bayes()
obj.read_file(file)
#obj.display()
obj.findProbability()







