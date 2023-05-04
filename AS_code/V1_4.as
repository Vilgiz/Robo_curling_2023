.AUXDATA
N_INT1    "io_calcERR  "
N_INT2    "io_start_game  "
N_INT3    "IO_STOP  "
N_INT4    "IO_NORMAL_SPEED  "
N_INT5    "IO_FAST_SPEED  "
N_INT6    "IO_DEPLOY_SPEED  "
N_INT7    "o_calcERR  "
.END
.INTER_PANEL_D
0,4,2,"","RUNNING","ENDING","",10,4,2,2003,0,0
1,3,"","START","MOVE","",10,1,13,0,0,2002,2002,0
2,8,"main_speed","MAIN","SPEED",10,15,4,2,0
4,8,"norm_spd","NORMAL","SPEED",10,15,4,2,0
5,8,"fast_spd","FAST","SPEED",10,15,4,2,0
6,8,"destroy_spd","DESTROY","SPEED",10,15,4,2,0
7,5,2,"MODE","DESTROY","FAST","NORMAL",10,2,3,4,2006,2005,2004,0
14,8,"Target_status","TARGET","NUMBER",10,3,4,2,0
16,10,"LEFT","","","",10,4,3,1,target_status = 1,0
17,10,"LEFTER","","","",10,4,3,2,target_status = 2,0
18,10,"CENTER","","","",10,4,3,3,Target_status = 3,0
19,10,"RIGHTER","","","",10,4,3,4,target_status = 4,0
20,10,"RIGHT","","","",10,4,3,5,target_status = 5,0
21,8,"Start_status","START","NUMBER",10,4,4,2,0
24,10,"LEFTER","","","",10,3,4,6,start_status = 2,0
25,10,"CENTER","","","",10,3,4,7,start_status = 3,0
26,10,"RIGHTER","","","",10,3,4,8,start_status = 4,0
27,8,"diff","RAZNOS","TOCHEK",10,15,4,2,0
.END
.INTER_PANEL_TITLE
"",0
"",0
"",0
"",0
"",0
"",0
"",0
"",0
.END
.INTER_PANEL_COLOR_D
182,3,224,244,28,159,252,255,251,255,0,31,2,241,52,219,
.END
.PROGRAM MAIN ()
  SPEED main_speed MM/S ALWAYS
  BASE NULL
  TWAIT(1)
  BASE FRAME (o1, x1, y1, o1)
  TWAIT(1)
  TOOL NULL
  TWAIT 1
  TOOL TRANS (0,0,139,-180,180,0)
  TWAIT 1
  PCABORT 5:
  PCEXECUTE 5: IF_offlin_ch.pc
  WHILE TRUE DO
    DO
      SWAIT io_start_game
      SPEED main_speed MM/S ALWAYS
      CALL GRAB
      CALL calculate_drop
      CALL DROP
    UNTIL IO_STOP <> TRUE
  END
.END
.PROGRAM TEACH () ; 
  BASE NULL
  TOOL NULL
  TOOL tool_calibr
  BREAK
  ALIGN
  LAPPRO o1,100
  LMOVE o1
  LMOVE y1
  LMOVE x1
  BREAK
  POINT base_coord = FRAME(o1,x1,y1,o1)
  BASE base_coord
  BREAK
  BREAK
  LMOVE TRANS(100,100,100)
  BREAK
  JMOVE #t_change
.END
.PROGRAM GRAB ()
  ACCURACY 1 ALWAYS
  LMOVE #Start_Pos
  LMOVE #Ready_Grab
  LMOVE #Pre_Grab
  BREAK
  SPEED grab_speed MM/S 
  LMOVE #Grab
  SPEED grab_speed*1.1 MM/S 
  DRAW ,,100
  LMOVE #Ready_to_drop
.END
.PROGRAM calculate_drop ()
  .R = Motion_rad - 50
  ;
   decompose .base[0] = frame (o1,x1,y1,o1)
  .dOz = .base[3] + .base[5]
  .dx = - (.base[0] * cos(.dOz) + .base[1] * sin(.dOz))
  .dy = - (.base[1] * cos(.dOz) - .base[0] * sin(.dOz))
   ;
  .x1 = DX (start_p)
  .x2 = DX (target_p)
  .y1 = DY (start_p)
  .y2 = DY (target_p)
  ;
  IF (.x2 == .x1) THEN
    POINT start_mp = TRANS (DX (start_p), DY(start_p), Zoffset, 0, 0, 0)
    POINT deploy_mp = TRANS (DX (start_p), minY + retract + 220, Zoffset, 0, 0, 0)
    POINT stop_mp = SHIFT (deploy_mp BY 0, -retract, 0)
  ELSE
    ;
    .k = (.y2 - .y1) / (.x2 - .x1)
    .m = .y1 - .k * .x1
    ;
    .a = .k*.k + 1
    .b = - 2 * (.k*.dy + .dx - .m*.k)
    .c = .dy*.dy - 2*.m*.dy + .m*.m + .dx*.dx - .R*.R
    .D = SQRT(.b*.b - 4*.a*.c)
    IF (.x2 < .x1) THEN
      .D = -.D
    END
    ;
    .rootX = (-.b + .D)/(2*.a)
    .rootY = .k * .rootX + .m
    .angle = ATAN2 (.x2-.x1, .y2-.y1)
    ;
    .x3 = retract * SIN(.angle)
    .y3 = retract * COS(.angle)
    ;  
    if ((.rootX > minX ) AND (.rootX < maxX ) AND (.rootY > minY + retract) AND (abs(.angle) < 90))AND (.rootY < maxY) THEN
    ;                            
      POINT start_mp = TRANS (DX (start_p), DY(start_p), Zoffset, 0, 0, -.angle)
      POINT deploy_mp = TRANS (.rootX, .rootY, Zoffset, 0, 0, -.angle)
      POINT stop_mp = SHIFT (deploy_mp BY -.x3, -.y3, 0)
    ELSE
      SIG o_calcERR
      POINT start_mp = TRANS (maxX/2, minY+30, Zoffset, 0, 0, 0)
      POINT deploy_mp = TRANS (maxX/2, minY + retract + 220, Zoffset, 0, 0, 0)
      POINT stop_mp = SHIFT (deploy_mp BY 0, -retract, 0)
    END
  END
.END
.PROGRAM DROP () ; 
  ;
  ACCEL acc ALWAYS
  DECEL dec ALWAYS
  ;
  LMOVE SHIFT(start_mp BY 0, 0, Zsafety)
  CP ON
  BREAK
  LMOVE start_mp
  ;
  ;.F = 
  ;.l = DX()
  ;
  ;
  ;
  ;
  ;
  IF SIG (IO_DEPLOY_SPEED) == TRUE THEN
    .spd = destroy_spd
    .acc = 100
    .dec = 80
  ELSE
    IF SIG (IO_FAST_SPEED) == TRUE THEN
      .spd = fast_spd
      .acc = 70
      .dec = 70
    ELSE ;normal
     .spd = norm_spd
      .acc = 60
      .dec = 60
    END
  END
  ;
  type .spd
  SPEED .spd
  ACCEL .acc
  DECEL .dec
  ;
  LMOVE deploy_mp
  BREAK
  LMOVE stop_mp
  DRAW 0,0, Zsafety
  JMOVE #Start_Pos
  CP OFF
.END
.PROGRAM init.pc ()
  ; Internal signals for IFP
  int_exec_main = 2900
  ; TCP/IP Settings
  tcp_port = 48569
  $tcp_ip = "10.208.31.161"
  tcp_send_time = 10
  tcp_conn_time = 10
  tcp_recv_time = 15
  socket_id = -1
  ; Other
  IFPWPRINT 1 = " "
  debug = TRUE
.END
.PROGRAM IF_offlin_ch.pc ()
  ; *******************************************************************
  ;
  ; Program:      IF_offlin_ch.pc
  ; Comment:      
  ; Author:       User
  ;
  ; Date:         5/2/2023
  ;
  ; *******************************************************************
  ;
  .centre = 400
  
  WHILE TRUE DO
  CASE Target_status OF
    VALUE 1:
      POINT target_p = TRANS(.centre - 2*diff,1100,0,0,0,0)
    VALUE 2:
      POINT target_p = TRANS(.centre - diff,1100,0,0,0,0)
    VALUE 3:
      POINT target_p = TRANS(.centre,1100,0,0,0,0)
    VALUE 4:
      POINT target_p = TRANS(.centre + diff,1100,0,0,0,0)
    VALUE 5:
      POINT target_p = TRANS(.centre + 2*diff,1100,0,0,0,0)
    ANY :
      POINT target_p = TRANS(.centre,1100,0,0,0,0)
  END
    
 CASE Start_status OF
    VALUE 2:
      POINT start_p = TRANS(.centre - diff,minY,0,0,0,0)
    VALUE 3:
      POINT start_p = TRANS(.centre,minY,0,0,0,0)
    VALUE 4:
      POINT start_p = TRANS(.centre + diff,minY,0,0,0,0)
    ANY :
      POINT start_p = TRANS(.centre,minY,0,0,0,0)
  END
 END
.END
.PROGRAM Comment___ () ; Comments for IDE. Do not use.
	; @@@ PROJECT @@@
	; @@@ PROJECTNAME @@@
	; V1_3_outOfTrans
	; @@@ HISTORY @@@
	; 23.04.2023 22:49:24
	; 
	; 26.04.2023 15:41:16
	; 
	; 02.05.2023 15:00:30
	; 
	; 03.05.2023 12:22:05
	; тесты
	; @@@ INSPECTION @@@
	; Target_status
	; @@@ CONNECTION @@@
	; RS007L
	; 192.168.2.228
	; 23
	; @@@ PROGRAM @@@
	; MainProg:MAIN
	; 0:MAIN:F
	; 0:TEACH:F
	; .pc 
	; 0:GRAB:F
	; 0:calculate_drop:F
	; .R 
	; .dx 
	; .dy 
	; .x1 
	; .x2 
	; .y1 
	; .y2 
	; .m 
	; .k 
	; .a 
	; .b 
	; .c 
	; .rootX 
	; .rootY 
	; .angle 
	; .x3 
	; .y3 
	; .base 
	; .dOz 
	; .D 
	; 0:DROP:F
	; .spd 
	; .acc 
	; .dec 
	; 0:init.pc:B
	; 0:IF_offlin_ch.pc:B
	; .centre 
	; .step 
	; @@@ TRANS @@@
	; @@@ JOINTS @@@
	; @@@ REALS @@@
	; maxX 
	; maxY 
	; minX 
	; minY 
	; Motion_rad 
	; Zoffset 
	; Zsafety 
	; Target_status 
	; Start_status 
	; @@@ STRINGS @@@
	; @@@ INTEGER @@@
	; @@@ SIGNALS @@@
	; io_calcERR 
	; io_start_game 
	; IO_STOP 
	; IO_NORMAL_SPEED 
	; IO_FAST_SPEED 
	; IO_DEPLOY_SPEED 
	; o_calcERR 
	; @@@ TOOLS @@@
	; @@@ BASE @@@
	; @@@ FRAME @@@
	; @@@ BOOL @@@
.END
.TRANS
tool_calibr -22.500000 22.500000 108.000000 0.000000 180.000000 180.000000
tool_rock 0.000000 0.000000 138.000000 -180.000000 180.000000 0.000000
he -514.120117 17.167391 -225.309174 0.000000 0.000000 0.000000
o1 -462.454071 -413.723663 -351.845703 0.055453 0.359477 90.153748
x1 462.086151 -513.723267 -351.845703 0.000000 0.000000 0.000000
y1 -747.174194 -414.771210 -351.527740 0.008914 0.359882 90.202751
.END
.JOINTS
#take1 -39.931789 28.146606 -88.212029 1.514356 -58.995213 -3.377170
#start_pos -91.265190 26.640381 -121.421951 0.640723 -31.712723 2.059593
#take -17.959133 37.498539 -93.167679 -179.896301 49.310764 -162.121216
#ready_to_drop -63.854298 29.110840 -117.963348 -0.875391 -28.019945 -24.144751
#ready_grab -47.772511 41.278202 -95.430435 0.258398 -43.027267 -42.554760
#pre_grab -54.164360 57.766846 -79.576904 1.999512 -38.276371 -36.878689
#p4 -45.774319 46.378784 -77.089706 1.545117 -55.394444 206.538116
#p3 -40.680176 49.244022 -72.092552 0.160840 -58.568806 25.348522
#p2 -51.674854 44.518066 -80.461739 0.210938 -54.912415 36.304710
#p1 -44.107475 39.614140 -89.787613 0.193359 -50.530933 28.738161
#he -88.097610 32.671150 -112.828773 0.008790 -34.389950 30.189280
#grab -57.816658 63.424442 -66.312744 0.136230 -45.271915 -31.032148
#glue -39.932232 32.316284 -90.783119 1.515234 121.103668 -3.377609
#end_pos -89.043320 19.166750 -155.709030 -19.043261 -7.385561 -0.279550
#drop_2 -88.541023 64.594116 -71.989037 -0.005273 -42.998428 -176.409409
#drop_1 -88.146828 53.255131 -99.587814 -0.002637 -26.772997 -176.804504
#c -51.674854 44.518066 -80.461739 0.210938 -54.912415 36.304710
#b -9.030323 47.351074 -60.883659 0.007031 -71.680984 0.020970
#a -44.107475 39.614140 -89.787613 0.194238 -50.530247 28.738174
.END
.REALS
diff = 100
main_speed = 70
grab_speed = 30
io_calcERR = 2001
acc = 50
dec = 50
maxX = 650
maxY = 850
minX = 130
minY = 10
Motion_rad = 800
retract = 100
io_start_game = 2002
Zoffset = 3
Zsafety = 120
IO_STOP = 2003
IO_NORMAL_SPEED = 2004
IO_FAST_SPEED = 2005
IO_DEPLOY_SPEED = 2006
Target_status = 0
Start_status = 0
o_calcERR = 2007
destroy_spd = 0
fast_spd = 0
norm_spd = 0
.END
