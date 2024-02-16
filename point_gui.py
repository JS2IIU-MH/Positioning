''' point_gui.py '''

import tkinter as tk

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class Application(tk.Frame):
    '''Application - class to define GUI widgets

        tkinter widgets will be defined in Application.__init__

        Args:
            None
        Returns:
            None
    '''

    def __init__(self, master):
        super().__init__(master)
        self.grid()

        # variables
        self.fixed_ax = 50
        self.fixed_ay = 50
        self.fixed_z = 0

        self.mov_ax = 50
        self.mov_ay = 50

        self.position = [5, -100, 10, 5]

        self.fix_pos = []
        self.mov_pos = []
        self.get_fix_pos()
        self.get_mov_pos()

        self.dist_cal16 = [0 for i in range(16)]
        self.dist_in16 = [0 for i in range(16)]
        self.dist_adj16 = [0 for i in range(16)]

        self.get_dist_cal16()

        self.build_window(master=master)


    def build_window(self, master):
        ''' build tk.Frames'''

        entry_width = 6
        label_width = 5

        frame_A = tk.Frame(master)

        # Frame A1
        frame_a1 = tk.Frame(frame_A)
        label_a1 = tk.Label(frame_a1, text='FIXED ST.')
        label_a1_ax = tk.Label(frame_a1, text='ax', width=label_width)
        label_a1_ay = tk.Label(frame_a1, text='ay', width=label_width)

        sv_a1_ax = tk.StringVar(value=str(self.fixed_ax))
        sv_a1_ay = tk.StringVar(value=str(self.fixed_ay))
        ent_a1_ax = tk.Entry(frame_a1, textvariable=sv_a1_ax, width=entry_width, justify=tk.CENTER)
        ent_a1_ay = tk.Entry(frame_a1, textvariable=sv_a1_ay, width=entry_width, justify=tk.CENTER)

        label_a1.grid(row=0, column=0, columnspan=2)
        label_a1_ax.grid(row=1, column=0)
        label_a1_ay.grid(row=2, column=0)
        ent_a1_ax.grid(row=1, column=1)
        ent_a1_ay.grid(row=2, column=1)

        frame_a1.grid()

        # Frame A2
        frame_a2 = tk.Frame(frame_A)

        label_a2 = tk.Label(frame_a2, text='MOVING ST.')
        label_a2_ax = tk.Label(frame_a2, text='ax', width=label_width)
        label_a2_ay = tk.Label(frame_a2, text='ay', width=label_width)

        sv_a2_ax = tk.StringVar(value=str(self.mov_ax))
        sv_a2_ay = tk.StringVar(value=str(self.mov_ay))
        ent_a2_ax = tk.Entry(frame_a2, textvariable=sv_a2_ax, width=entry_width, justify=tk.CENTER)
        ent_a2_ay = tk.Entry(frame_a2, textvariable=sv_a2_ay, width=entry_width, justify=tk.CENTER)

        label_a2.grid(row=0, column=0, columnspan=2)
        label_a2_ax.grid(row=1, column=0)
        label_a2_ay.grid(row=2, column=0)
        ent_a2_ax.grid(row=1, column=1)
        ent_a2_ay.grid(row=2, column=1)

        frame_a2.grid()

        # Frame A3
        frame_a3 = tk.Frame(frame_A)

        label_a3 = tk.Label(frame_a3, text='POSITION')
        label_a3_x = tk.Label(frame_a3, text='X', width=label_width)
        label_a3_y = tk.Label(frame_a3, text='Y', width=label_width)
        label_a3_z = tk.Label(frame_a3, text='Z', width=label_width)
        label_a3_th = tk.Label(frame_a3, text='TH', width=label_width)

        sv_a3_x = tk.StringVar(value=str(self.position[0]))
        sv_a3_y = tk.StringVar(value=str(self.position[1]))
        sv_a3_z = tk.StringVar(value=str(self.position[2]))
        sv_a3_th = tk.StringVar(value=str(self.position[3]))

        ent_a3_x = tk.Entry(frame_a3, textvariable=sv_a3_x, width=entry_width, justify=tk.CENTER)
        ent_a3_y = tk.Entry(frame_a3, textvariable=sv_a3_y, width=entry_width, justify=tk.CENTER)
        ent_a3_z = tk.Entry(frame_a3, textvariable=sv_a3_z, width=entry_width, justify=tk.CENTER)
        ent_a3_th = tk.Entry(frame_a3, textvariable=sv_a3_th, width=entry_width, justify=tk.CENTER)

        label_a3.grid(row=0, column=0, columnspan=2)
        label_a3_x.grid(row=1, column=0)
        label_a3_y.grid(row=2, column=0)
        label_a3_z.grid(row=3, column=0)
        label_a3_th.grid(row=4, column=0)

        ent_a3_x.grid(row=1, column=1)
        ent_a3_y.grid(row=2, column=1)
        ent_a3_z.grid(row=3, column=1)
        ent_a3_th.grid(row=4, column=1)

        frame_a3.grid()

        frame_A.grid(row=0, column=0)


        # Frame B
        frame_B = tk.Frame(master)
        self.draw_graph(frame_B)

        frame_B.grid(row=0, column=1)

        # Frame C
        frame_C = tk.Frame(master)

        frame_c1 = tk.Frame(frame_C)
        
        self.draw_matrix(frame_c1, self.dist_cal16, 'Distance')

        frame_c1.grid()

        frame_c2 = tk.Frame(frame_C)
        self.draw_matrix(frame_c2, self.dist_in16, 'Input')

        frame_c2.grid()

        frame_c3 = tk.Frame(frame_C)

        frame_c3.grid()

        frame_C.grid(row=0, column=2)

    def get_fix_pos(self):
        self.fix_pos = [[- self.fixed_ax / 2, self.fixed_ay / 2, self.fixed_z],
                        [self.fixed_ax / 2, self.fixed_ay / 2, self.fixed_z],
                        [- self.fixed_ax / 2, - self.fixed_ay / 2, self.fixed_z],
                        [self.fixed_ax / 2, - self.fixed_ay / 2, self.fixed_z]]

    def get_mov_pos(self):
        # self.position = [5, -50, 10, 5]
        if self.position[3] != 0:
            angle_rad = self.position[3] / 180 * np.pi
        
        r_cos = np.cos(angle_rad)
        r_sin = np.sin(angle_rad)

        X = self.position[0]
        Y = self.position[1]

        px = self.mov_ax / 2
        py = self.mov_ay / 2
        pz = self.position[2]

        self.mov_pos = [[- px * r_cos + py * (-r_sin) + X, - px * r_sin + py * r_cos + Y, pz],
                        [px * r_cos + py * (-r_sin) + X, px * r_sin + py * r_cos + Y, pz],
                        [- px * r_cos - py * (-r_sin) + X, - px * r_sin - py * r_cos + Y, pz],
                        [px * r_cos - py * (-r_sin) + X, px * r_sin - py * r_cos + Y, pz]]
        
    def draw_matrix(self, master, list_data, matrix_title):
        ''' GUI 4x4マトリクスを表示 '''
        CELL_WIDTH = 5
        i = 0
        entry_list = [0 for i in range(16)]
        sv_list = [0 for i in range(16)]

        mat_label = tk.Label(master, text=matrix_title)
        mat_label.grid(row=0, column=0, columnspan=4)
        for row in range(4):
            for col in range(4):
                sv_list[i] = tk.StringVar(value=f'{list_data[i]:3.0f}')
                entry_list[i] = tk.Entry(master, textvariable=sv_list[i], width=CELL_WIDTH, justify=tk.CENTER)
                entry_list[i].grid(row=row+1, column=col)
                i += 1

        #     self.dist_cal16 = [0 for i in range(16)]
        # self.dist_in16 = [0 for i in range(16)]
        # self.dist_adj16 = [0 for i in range(16)]

    def get_dist_cal16(self):
        # self.fix_posとself.mov_posのユニット間距離を計算する
        i = 0
        for mov in range(4):
            for fix in range(4):
                self.dist_cal16[i] = self.calc_dist(self.mov_pos[mov], self.fix_pos[fix])
                i += 1

    @classmethod
    def calc_dist(cls, p1, p2):
        dist = np.sqrt(
            np.power(p2[0] - p1[0], 2) + np.power(p2[1] - p1[1], 2) + np.power(p2[2] - p1[2], 2)
        )
        return dist

    def draw_graph(self, master):
        ''' matplotlib graph on tkinter '''
        pf = self.fix_pos
        pm = self.mov_pos

        fig, ax = plt.subplots()
        fig.set_figwidth(1)
        fig.set_figheight(2)

        h_fix, = ax.plot([pf[i][0] for i in range(4)], [pf[i][1] for i in range(4)], color='blue')
        h_mov, = ax.plot([pm[i][0] for i in range(4)], [pm[i][1] for i in range(4)], color='red')
        ax.set_xlim(-100, 100)
        ax.set_ylim(-400, 50)
        ax.grid()

        # canvas
        canvas = FigureCanvasTkAgg(fig, master=master)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.grid()



    def update_graph(self):
        pass




def main():
    '''example to call Application class'''

    root = tk.Tk()

    root.geometry('600x500')
    root.title('tkinter template')
    root.grid_anchor(tk.CENTER)

    app = Application(master=root)
    app.mainloop()


if __name__ == "__main__":
    main()