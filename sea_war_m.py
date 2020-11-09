import random

class Ship():
    def __init__(self,fl,field_size=6):        
        self.fz=field_size
        self.fl=fl
        self.sh_conf=None
        self.shoot={}
        self.gen_shot=[(x%self.fz,x//self.fz) for x in range(self.fz**2)]
        self.win=None
    def create_ship(self):        
        dict_ship={1:[],2:[],3:[]}        
        for k in dict_ship.keys():
            dict_ship[k]=list(filter(lambda x: len(x)>0,[[(c[0]+x,c[1]) for x in range(k) if c[0]+k-1<self.fz] for c in self.fl.keys()]))+list(filter(lambda x: len(x)>0,[[(c[0],c[1]+y) for y in range(k) if c[1]+k-1<self.fz] for c in self.fl.keys()]))
        ship_type=[3,2,2,1,1,1,1]
        self.win=len(ship_type)
        fill=True
        while fill:
            ship_config=set()
            fill_site=set()
            self.sh_conf=[]
            for k in ship_type:
                cur_ship=dict_ship[k]
                while True:
                    cur_site=cur_ship[random.randint(0,len(cur_ship)-1)] 
                    if all([1 if cs not in fill_site else 0 for cs in cur_site]):
                        ship_config.update({cs for cs in cur_site})                
                        shadow_site=[[(xy[0]+dx,xy[1]+dy) for dx in (-1,0,1) for dy in (-1,0,1)] for xy in cur_site]
                        self.sh_conf.append(['no damage',{cs:'*' for cs in cur_site},{s for shst in shadow_site for s in shst if (-1<s[0]<self.fz) and (-1<s[1]<self.fz)}.difference({cs for cs in cur_site}),k])                        
                        fill_site.update({s for shst in shadow_site for s in shst if (-1<s[0]<self.fz) and (-1<s[1]<self.fz)})                
                        break
                    elif len(fill_site)==len(self.fl):
                        break
                if len(fill_site)==len(self.fl):
                    break
            if len(ship_config)>=sum(ship_type):
                break
        return self.sh_conf        
    def get_ship(self):
        return self.sh_conf
    def set_ship(self):
        pass    
    def shooting(self,st):
        mov=0
        if st not in self.shoot:            
            for sc in self.sh_conf:
                dmg=0
                total_dmg=0
                if st in sc[1].keys():
                    sc[1][st]='X'
                    self.shoot[st]='X'
                    dmg=sum(list([1 if sc[1][s]=='X' else 0 for s in sc[1].keys()]))                    
                    if dmg==sc[3]:
                        sc[0]='sink'
                        total_dmg=sum(list([1 if sc[0]=='sink' else 0 for sc in self.sh_conf]))                        
                        if total_dmg>=self.win:
                            for s in sc[2]:
                                if s not in self.shoot:
                                    self.shoot[s]='T'
                            mov=4
                            break                                
                        for s in sc[2]:
                            if s not in self.shoot:
                                self.shoot[s]='T'
                        mov=2 
                        break    
                    elif 0<dmg<sc[3]:
                        sc[0]='hit'
                        mov=1
                        break
                else:
                    self.shoot[st]='T'
                    mov=0          
        else:
            mov=3            
        return mov,self.shoot,self.sh_conf    
    def generate_shot(self,pl):
        point=set()
        if pl==1:
            correct=False
            while not correct: 
                try:
                    instr=input('введите координаты через пробел: ').split(' ')
                    point=(int(instr[0]),int(instr[1]))
                    if (point in self.gen_shot) and (point not in self.shoot.keys()):
                        correct=True
                    else:
                        print('Ошибка ввода')
                except Exception:
                    print('Ошибка ввода')
        else:
            for k in self.shoot.keys():
                if k in self.gen_shot:
                    self.gen_shot.remove(k)            
            sh=random.randint(0,len(self.gen_shot)-1)
            point=(self.gen_shot[sh][0],self.gen_shot[sh][1])
        return point    
                
class Board():
    def __init__(self,field_size=6):
        self.fz=field_size
        self.fl=None
        self.head=[' ' if i==0 else i-1 for i in range(self.fz+1)]
    def set_board(self):
        self.fl={'own':{(x%self.fz,x//self.fz):'O' for x in range(self.fz**2)},'enemy':{(x%self.fz,x//self.fz):'O' for x in range(self.fz**2)}}        
        return self.fl
    def get_board(self,ft):
        return self.fl[ft]
    def view_board(self,fl_own,fl_enm,sh_own_conf=None,own_shoot=None,sh_enm_conf=None,enm_shoot=None):
        if sh_own_conf is not None:
            for el in sh_own_conf:
                for k,v in el[1].items():
                    if k in fl_own:
                        fl_own[k]=v
        if own_shoot is not None:
            for k,v in own_shoot.items():
                if k in fl_own:
                    fl_own[k]=v                 
        if enm_shoot is not None:
            for k,v in enm_shoot.items():
                if k in fl_enm:
                    fl_enm[k]=v        
        all_field_own=[self.head if i==0 else [self.head[i] if j==0 else fl_own[(j-1,i-1)] for j in range(self.fz+1)] for i in range(self.fz+1)]  
        all_field_enm=[self.head if i==0 else [self.head[i] if j==0 else fl_enm[(j-1,i-1)] for j in range(self.fz+1)] for i in range(self.fz+1)]        
        for i in range(self.fz+1):
            str_own,str_enm='',''
            for j in range(self.fz+1):                
                str_own+=f"{all_field_own[i][j]} | "
                str_enm+=f"{all_field_enm[i][j]} | "
            print(str_own+' '*10+str_enm)
            print('-'*27+' '*10+'-'*27)
    def first_step(self):
        hs=random.randint(0,1)
        if hs==0:        
            return 1,2
        else:
            return 2,1 
game={1:{'stat':None,'all_shoot':None,'ship_conf':None},2:{'stat':None,'all_shoot':None,'ship_conf':None}}            
bd=Board()
ini_field=bd.set_board()
player_1=Ship(bd.get_board('own'))
player_2=Ship(bd.get_board('own'))
game[1]['ship_conf']=player_1.create_ship()
game[2]['ship_conf']=player_2.create_ship()
bd.view_board(ini_field['own'],ini_field['enemy'],game[2]['ship_conf'])
new_game=True
while new_game:
    cur_step=True
    while cur_step:
        pp=player_1.generate_shot(1)
        game[1]['stat'],game[1]['all_shoot'],game[1]['ship_conf']=player_1.shooting(pp)
        if game[1]['stat']==4:
            print('Последний корабль потоплен, вы выйграли')
            new_game=False
            break    
        elif game[1]['stat']==3:
            print('Ошибка ввода')
        elif game[1]['stat']==2:
            print('Потопил, ходи ишо раз')            
        elif game[1]['stat']==1:
            print('Подбил, ходи ишо раз')            
        else:
            print('Промазал, ход переходит')            
            cur_step=False
        bd.view_board(ini_field['own'],ini_field['enemy'],game[2]['ship_conf'],game[2]['all_shoot'],game[1]['ship_conf'],game[1]['all_shoot'])        
    if new_game:
        cur_step=True
        while cur_step:
            pp=player_2.generate_shot(2)
            print(f"Ходит компьютер: {pp}")
            game[2]['stat'],game[2]['all_shoot'],game[2]['ship_conf']=player_2.shooting(pp)
            if game[2]['stat']==4:
                print('Компьютер потопил последний корабль, и выйграл')
                new_game=False
                break    
            elif game[2]['stat']==3:
                print('Ошибка ввода')
            elif game[2]['stat']==2:
                print('Компьютер потопил, ходит ишо раз')            
            elif game[2]['stat']==1:
                print('Компьютер подбил, ходит ишо раз')            
            else:
                print('Компьютер промазал, ход переходит')            
                cur_step=False
            bd.view_board(ini_field['own'],ini_field['enemy'],game[2]['ship_conf'],game[2]['all_shoot'],game[1]['ship_conf'],game[1]['all_shoot'])    
        






    
    
    
    