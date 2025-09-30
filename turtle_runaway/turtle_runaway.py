# This example is not working in Spyder directly (F5 or Run)
# Please type '!python turtle_runaway.py' on IPython console in your Spyder.
import tkinter as tk
import turtle, random

# 감옥 위치와 출구 설정
JAIL_SIZE = 100
JAIL_CENTER = (-250, 250)  # 감옥을 좌측 상단으로 이동
EXIT_POS = (250, -250)     # 출구를 우측 하단으로 이동
EXIT_RADIUS = 20  # 출구 판정 반경

class RunawayGame:
    def __init__(self, canvas, runner, chaser, catch_radius=50):
        self.canvas = canvas
        self.runner = runner
        self.chaser = chaser
        self.catch_radius2 = catch_radius**2

        # Initialize 'runner' and 'chaser'
        self.runner.shape('turtle')
        self.runner.color('blue')
        self.runner.penup()

        self.chaser.shape('turtle')
        self.chaser.color('red')
        self.chaser.penup()

        # Instantiate another turtle for drawing
        self.drawer = turtle.RawTurtle(canvas)
        self.drawer.hideturtle()
        self.drawer.penup()
        self.game_over = False
        self.time_elapsed = 0  # 시간 측정용

    def is_catched(self):
        p = self.runner.pos()
        q = self.chaser.pos()
        dx, dy = p[0] - q[0], p[1] - q[1]
        return dx**2 + dy**2 < self.catch_radius2

    def is_escaped(self):
        # 출구 근처에 도달하면 탈출 성공
        rx, ry = self.runner.pos()
        ex, ey = EXIT_POS
        return ((rx - ex) ** 2 + (ry - ey) ** 2) < EXIT_RADIUS ** 2

    def start(self, init_dist=400, ai_timer_msec=100):
        self.canvas.bgcolor("lightgreen")
        self.draw_jail_and_exit()
        # runner를 감옥 중앙에, chaser를 오른쪽에 배치
        self.runner.setpos(JAIL_CENTER)
        self.runner.setheading(0)
        self.chaser.setpos((+init_dist / 2, 0))
        self.chaser.setheading(180)

        self.ai_timer_msec = ai_timer_msec
        self.time_elapsed = 0
        self.game_over = False
        self.canvas.ontimer(self.step, self.ai_timer_msec)

    def draw_jail_and_exit(self):
        jail = turtle.RawTurtle(self.canvas)
        jail.hideturtle()
        jail.speed(0)
        jail.pensize(3)
        jail.penup()
        # 감옥 사각형
        x0, y0 = JAIL_CENTER[0] - JAIL_SIZE // 2, JAIL_CENTER[1] - JAIL_SIZE // 2
        jail.goto(x0, y0)
        jail.pendown()
        for i in range(4):
            if i == 1:
                # 출구 부분: 오른쪽 벽 중간에 출구를 그림
                jail.forward(JAIL_SIZE // 2 - EXIT_RADIUS)
                jail.penup()
                jail.forward(EXIT_RADIUS * 2)
                jail.pendown()
                jail.forward(JAIL_SIZE // 2 - EXIT_RADIUS)
            else:
                jail.forward(JAIL_SIZE)
            jail.left(90)
        # 감옥 세로 철창
        jail.penup()
        for i in range(1, 4):
            jail.goto(x0 + i * (JAIL_SIZE // 4), y0)
            jail.setheading(90)
            jail.pendown()
            jail.forward(JAIL_SIZE)
            jail.penup()
        # 출구 표시 (원)
        jail.goto(EXIT_POS[0], EXIT_POS[1] - EXIT_RADIUS)
        jail.pencolor("orange")
        jail.pendown()
        jail.circle(EXIT_RADIUS)
        jail.penup()
        jail.pencolor("black")

    def step(self):
        if self.game_over:
            return

        self.runner.run_ai(self.chaser.pos(), self.chaser.heading())
        self.chaser.run_ai(self.runner.pos(), self.runner.heading())

        is_catched = self.is_catched()
        is_escaped = self.is_escaped()
        self.drawer.undo()
        self.drawer.penup()
        self.drawer.setpos(-300, 300)
        self.drawer.write(f'Is catched? {is_catched}   Time: {self.time_elapsed/10:.1f}s')

        if is_catched:
            self.canvas.bgcolor("red")
            self.runner.color("gray")
            self.drawer.setpos(-80, 0)
            self.drawer.write("I got ya!", font=("Arial", 24, "bold"))
            self.game_over = True
            return  # 게임 종료

        if is_escaped:
            self.canvas.bgcolor("yellow")
            self.runner.color("gray")
            self.drawer.setpos(-80, 0)
            self.drawer.write("escape!!", font=("Arial", 24, "bold"))
            self.game_over = True
            return  # 게임 종료

        self.time_elapsed += 1
        self.canvas.ontimer(self.step, self.ai_timer_msec)

class MouseMover(turtle.RawTurtle):
    def __init__(self, canvas, step_move=20):
        super().__init__(canvas)
        self.step_move = step_move
        self.canvas = canvas
        self.target = None  # 클릭 목표 위치
        canvas.onclick(self.go_to_click)
        canvas.listen()

    def go_to_click(self, x, y):
        self.target = (x, y)

    def run_ai(self, opp_pos, opp_heading):
        if self.target:
            x, y = self.target
            angle = self.towards(x, y)
            self.setheading(angle)
            distance = self.distance(x, y)
            move = min(self.step_move, distance)
            self.forward(move)
            # 목표에 거의 도달하면 멈춤
            if distance < self.step_move:
                self.target = None

class RandomMover(turtle.RawTurtle):
    def __init__(self, canvas, step_move=10, step_turn=10):
        super().__init__(canvas)
        self.step_move = step_move
        self.step_turn = step_turn

    def run_ai(self, opp_pos, opp_heading):
        mode = random.randint(0, 2)
        if mode == 0:
            self.forward(self.step_move)
        elif mode == 1:
            self.left(self.step_turn)
        elif mode == 2:
            self.right(self.step_turn)

class ChaserMover(turtle.RawTurtle):
    def __init__(self, canvas, step_move=10, step_turn=10):
        super().__init__(canvas)
        self.step_move = step_move
        self.step_turn = step_turn

    def run_ai(self, opp_pos, opp_heading):
        # 도망자 쪽으로 방향을 맞추고 전진
        self.setheading(self.towards(opp_pos))
        self.forward(self.step_move)

if __name__ == '__main__':
    # Use 'TurtleScreen' instead of 'Screen' to prevent an exception from the singleton 'Screen'
    root = tk.Tk()
    canvas = tk.Canvas(root, width=700, height=700)
    canvas.pack()
    screen = turtle.TurtleScreen(canvas)

    # runner: 마우스 클릭으로 조종(회색), chaser: AI가 추격(회색)
    runner = MouseMover(screen)
    chaser = ChaserMover(screen)

    game = RunawayGame(screen, runner, chaser)
    game.start()
    screen.mainloop()