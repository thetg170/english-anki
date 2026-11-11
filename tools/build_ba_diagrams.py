#!/usr/bin/env python3
"""Build small original BA teaching diagrams as SVG; no external assets."""
from pathlib import Path
from html import escape
import shutil
import subprocess

OUT = Path(__file__).resolve().parents[1] / "source/business-analysis/media"
OUT.mkdir(parents=True, exist_ok=True)

class Drawing:
    def __init__(self, title, width=900, height=360):
        self.w, self.h = width, height
        self.parts = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" role="img" aria-label="{escape(title)}">',
                      '<defs><marker id="arrow" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0 0 L8 4 L0 8 Z" fill="#334155"/></marker></defs>',
                      '<rect width="100%" height="100%" fill="#ffffff"/>']
        self.text(width/2, 30, title, 20, weight="700")
    def add(self, s): self.parts.append(s)
    def text(self,x,y,s,size=15,weight="400",anchor="middle",fill="#172033"):
        self.add(f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-family="Arial,Helvetica,sans-serif" font-size="{size}" font-weight="{weight}" fill="{fill}">{escape(s)}</text>')
    def line(self,x1,y1,x2,y2,arrow=True,dash=False):
        self.add(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#334155" stroke-width="2"'+(' stroke-dasharray="6 5"' if dash else '')+(' marker-end="url(#arrow)"' if arrow else '')+'/>')
    def box(self,x,y,w,h,label,fill="#eff6ff",rx=13):
        self.add(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="#334155" stroke-width="2"/>')
        self.text(x+w/2,y+h/2+5,label,15,"600")
    def circle(self,x,y,r=19,thick=False,fill="#fff"):
        self.add(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}" stroke="#334155" stroke-width="{4 if thick else 2}"/>')
    def diamond(self,x,y,label):
        self.add(f'<polygon points="{x},{y-29} {x+29},{y} {x},{y+29} {x-29},{y}" fill="#fff7ed" stroke="#334155" stroke-width="2"/>')
        self.text(x,y+7,label,22,"700")
    def oval(self,x,y,w,h,label):
        self.add(f'<ellipse cx="{x}" cy="{y}" rx="{w/2}" ry="{h/2}" fill="#eff6ff" stroke="#334155" stroke-width="2"/>')
        self.text(x,y+5,label,15,"600")
    def actor(self,x,y,label):
        self.circle(x,y,12)
        self.line(x,y+12,x,y+63,False)
        self.line(x-22,y+31,x+22,y+31,False)
        self.line(x,y+63,x-20,y+89,False)
        self.line(x,y+63,x+20,y+89,False)
        self.text(x,y+115,label,14)
    def save(self,name):
        self.add('</svg>')
        (OUT/name).write_text('\n'.join(self.parts)+'\n',encoding='utf-8')

# BPMN: start event, task, exclusive gateway, end events.
d=Drawing("BPMN: event, task và gateway")
d.circle(95,175);d.text(95,225,"Start event",14)
d.box(195,140,170,70,"Kiểm tra đơn");d.text(280,235,"Task = việc cần làm",14)
d.diamond(485,175,"×");d.text(485,235,"Gateway = rẽ nhánh",14)
d.circle(750,105,20,True);d.circle(750,245,20,True)
d.text(750,75,"Hợp lệ");d.text(750,290,"Không hợp lệ")
d.line(115,175,195,175);d.line(365,175,456,175)
d.line(514,175,620,105,False);d.line(620,105,730,105)
d.line(514,175,620,245,False);d.line(620,245,730,245)
d.save("ba-bpmn-elements.svg")

# BPMN gateway semantics: exclusive picks one path; parallel requires both.
d=Drawing("BPMN: chọn một hay chạy cả hai",900,430)
d.text(220,75,"Exclusive gateway (×)",17,"700");d.diamond(220,190,"×")
d.box(385,110,150,54,"Thẻ");d.box(385,230,150,54,"Chuyển khoản")
d.line(249,175,385,137);d.line(249,205,385,257)
d.text(300,112,"chọn 1",13,fill="#475569")
d.text(680,75,"Parallel gateway (+)",17,"700");d.diamond(680,190,"+")
d.box(735,110,140,54,"Kiểm tra kho");d.box(735,230,140,54,"Chống gian lận")
d.line(709,175,735,137);d.line(709,205,735,257)
d.text(680,345,"Cả hai nhánh đều được kích hoạt.",14,fill="#475569")
d.save("ba-bpmn-gateways.svg")

# BPMN lanes: responsibilities and handoff inside one process pool.
d=Drawing("BPMN: lane cho biết ai thực hiện bước nào",900,360)
d.add('<rect x="60" y="80" width="780" height="225" fill="#fff" stroke="#334155" stroke-width="2"/>')
d.add('<line x1="60" y1="190" x2="840" y2="190" stroke="#94a3b8" stroke-width="2"/>')
d.text(130,140,"CS",17,"700");d.text(130,250,"Kho",17,"700")
d.line(190,80,190,305,False)
d.box(255,110,170,56,"Tiếp nhận đơn")
d.box(565,218,170,56,"Soạn hàng")
d.line(425,138,500,138,False);d.line(500,138,500,246,False);d.line(500,246,565,246)
d.text(500,330,"Mũi tên qua lane = bàn giao công việc",14,fill="#475569")
d.save("ba-bpmn-lanes.svg")

# UML use case: an actor outside the system boundary and goal ovals inside.
d=Drawing("UML use case: mục tiêu của actor với hệ thống",900,390)
d.actor(120,120,"Khách hàng")
d.add('<rect x="300" y="75" width="520" height="270" fill="#fff" stroke="#334155" stroke-width="2"/>')
d.text(560,103,"Hệ thống đặt hàng",16,"700")
for y,label in ((150,"Tạo đơn"),(225,"Tra cứu đơn"),(300,"Hủy đơn")):
    d.oval(580,y,225,58,label)
    d.line(155,166,468,y,False)
d.text(560,370,"Oval = mục tiêu tương tác; không phải màn hình.",14,fill="#475569")
d.save("ba-uml-use-case.svg")

# UML sequence: time flows downward and messages cross lifelines.
d=Drawing("UML sequence: thứ tự gọi API",900,460)
for x,label in ((120,"Ứng dụng"),(440,"Customer API"),(740,"Order API")):
    d.box(x-90,75,180,48,label,rx=4)
    d.line(x,123,x,405,False,True)
d.line(120,175,440,175);d.text(280,164,"1. Tạo khách hàng",14)
d.line(440,220,120,220,True,True);d.text(280,211,"2. Trả customerId",14)
d.line(120,285,740,285);d.text(430,275,"3. Tạo đơn với customerId",14)
d.line(740,335,120,335,True,True);d.text(430,326,"4. Trả mã đơn hoặc lỗi",14)
d.text(450,440,"Đọc từ trên xuống: không tạo đơn trước khi có customerId.",14,fill="#475569")
d.save("ba-uml-sequence.svg")

# UML state: one object's lifecycle; transitions are labeled.
d=Drawing("UML state: trạng thái và điều kiện chuyển",900,410)
d.circle(70,190,9,False,"#172033")
for x,label in ((155,"Draft"),(355,"Paid"),(555,"Shipped"),(755,"Refunded")):
    d.box(x,160,125,60,label,rx=18)
d.line(79,190,155,190)
for x1,x2,label in ((280,355,"thanh toán"),(480,555,"giao hàng"),(680,755,"hoàn tiền")):
    d.line(x1,190,x2,190);d.text((x1+x2)/2,170,label,13)
d.text(220,295,"Draft: có thể sửa",14);d.text(420,295,"Paid: không sửa",14)
d.text(450,365,"Mỗi mũi tên cần điều kiện và người có quyền thực hiện.",14,fill="#475569")
d.save("ba-uml-state.svg")

# Data model: fields and key relation.
d=Drawing("Dữ liệu: primary key và foreign key",900,380)
d.box(90,115,265,170,"",rx=4);d.box(545,115,265,170,"",rx=4)
for x,title,fields in ((90,"Customer",["id  PK","name"]),(545,"Order",["id  PK","customer_id  FK","total"])):
    d.text(x+132,145,title,18,"700")
    d.line(x,160,x+265,160,False)
    for n,label in enumerate(fields):d.text(x+25,190+n*28,label,15,anchor="start")
d.line(545,215,355,215)
d.text(450,202,"tham chiếu",14,fill="#475569")
d.text(450,340,"Order.customer_id tham chiếu Customer.id",15,fill="#475569")
d.save("ba-data-keys.svg")

renderer = shutil.which("rsvg-convert")
if renderer:
    for svg in OUT.glob("ba-*.svg"):
        subprocess.run([renderer, "-w", "1200", str(svg), "-o", str(svg.with_suffix(".png"))], check=True)
print("generated 7 original diagrams in", OUT)
