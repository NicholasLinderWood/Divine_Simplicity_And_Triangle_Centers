'''Run this script to interactively learn about triangles and triangle centers.
    See the github page for more information on how this relates to the doctrine
    of divine simplicity.
    
    Name: Nicholas Wood, PhD
    Institution: USNA
    Email: nwood@usna.edu
'''
from matplotlib import pyplot as plt
from Geometry import Triangle, LineSegment
from matplotlib.widgets import Button
import numpy as np
import math
from random import random


class TriangleViewer:

    def __init__(self):

        #Store the index of the vertex we are clicked on
        #initially None
        self.vind = None

        #Additionally store the maximum distance a vertex can be
        #from the click in order for it to register
        self.epsilon = 0.1

        #Initialize the figure
        self.Initialize_Figure()

        #Initially draw the triangle
        self.Draw_Triangle()

        #Initialize the triangle centers
        self.Draw_Centers()

        #Create buttons for the centers
        self.Create_Center_Buttons()

        #Create randomize button
        self.Create_Random_Button()

        #Create Reset button
        self.Create_Reset_Button()

        #Show the triangle
        plt.show()


    def Initialize_Figure(self):

        #Generate a figure
        fig = plt.figure(figsize = (16, 9))

        #Store the triangle line width
        self._triangle_linewidth = 6

        #Store center line_width
        self._center_linewidth = 3

        #Store center size
        self._center_size = 20

        #Create an axis object with will be used to plot the triangle
        #and centers
        ax = fig.add_axes([0.2, 0.2, 0.7, 0.7])

        ax.set_title('Divine Simplicity and\nTriangle Centers', fontsize = 28)

        #Set the aspect ratio of the axis to equal
        ax.set_aspect('equal')

        #Rescale the initialized triangle so it is contained in the 1x1 box
        ax.set_xlim([0, 1])
        ax.set_ylim([0, 1])

        #Add a grid
        ax.grid(zorder = 1)

        #Turn remove ticks
        ticks, labels = plt.xticks()
        plt.xticks(ticks = ticks, labels = ['' for t in ticks])
        ticks, labels = plt.yticks()
        plt.yticks(ticks = ticks, labels = ['' for t in ticks])


        #connect the mouse movements and clicks to this figure
        fig.canvas.mpl_connect('button_press_event', self.mouse_click_callback)
        fig.canvas.mpl_connect('button_release_event', self.mouse_release_callback)
        fig.canvas.mpl_connect('motion_notify_event', self.mouse_movement_callback)

        self.triangle_axis = ax
        self.fig = fig

        

    def Draw_Triangle(self):


        #Initialize an equilateral triangle
        A = np.array([0.25, 0.25])
        B = np.array([0.5, math.sqrt(0.5**2 - 0.25**2) + 0.25])
        C = np.array([0.75, 0.25])
        triangle = Triangle(A, B, C)


        ax = self.triangle_axis


        #Generate the triangle and add it to the plot
        X, Y = triangle.Generate_Triangle()
        triangle_lines = ax.plot(X, Y, 'k', linewidth = self._triangle_linewidth, zorder = 3)

        #Add axis, and triangle to the TriangleViewer
        self.triangle_lines = triangle_lines
        self.triangle = triangle

    def Draw_Centers(self):

        triangle = self.triangle
        ax = self.triangle_axis


        #Determines the colors of the centers/lines to be drawn
        centercolors = {'Centroid':'b', 'Incenter':'r', 'Circumcenter':'g', 'Orthocenter':'y'}

        centers = centercolors.keys()

        #0 -> No draw, 1 -> Draw 1 line, 2 Draw center and lines, 3 -> Draw center only
        #Initially set all to zero
        center_draw_flags = {center:0 for center in centers}

        #Create axes for centers and lines
        center_lines = {center: [ax.plot([], [], centercolors[center], linestyle = '--', linewidth = self._center_linewidth, zorder = 2) for i in range(3)] for center in centers}
        center_points = {center: ax.plot([], [], centercolors[center] + 'o', markersize = self._center_size, markeredgecolor = 'k', zorder = 2) for center in centers}


        self.inscribed = ax.plot([], [], centercolors['Incenter'], linestyle = '-', linewidth = self._center_linewidth, zorder = 2)
        self.circumscribed = ax.plot([], [], centercolors['Circumcenter'], linestyle = '-', linewidth = self._center_linewidth, zorder = 2)
        self.center_lines = center_lines
        self.center_points = center_points
        self.center_draw_flags = center_draw_flags
        self.centers = centers


    def Create_Center_Buttons(self):

        centers = self.centers
        fig = self.fig


        buttons = []
        for i, center in enumerate(centers):

            ax = fig.add_axes([0.35 + i*0.105, 0.1, 0.09, 0.06])
            buttons.append(Button(ax, center))

        for button in buttons:
            center = button.label.get_text()

            if center == 'Centroid':
                button.on_clicked(self.centroid_button_click)

            elif center == 'Incenter':
                button.on_clicked(self.incenter_button_click)

            elif center == 'Circumcenter':
                button.on_clicked(self.circumcenter_button_click)

            elif center == 'Orthocenter':
                button.on_clicked(self.orthocenter_button_click)

        for button in buttons:
            button.label.set_fontsize(14)


        self.center_buttons = buttons

    def Create_Reset_Button(self):

        fig = self.fig
        ax = fig.add_axes([0.1, 0.60, 0.125, 0.075])
        reset_button = Button(ax, 'Reset')
        reset_button.label.set_fontsize(20)

        reset_button.on_clicked(self.reset_button_click)

        self.reset_button = reset_button

    def reset_button_click(self, event):
        
        ax = self.triangle_axis

        [inscribed] = self.inscribed
        [circumscribed] = self.circumscribed

        inscribed.set_xdata([])
        inscribed.set_ydata([])
        circumscribed.set_xdata([])
        circumscribed.set_ydata([])


        centers = self.centers

        center_draw_flags = {center:0 for center in centers}

        Center_Lines = self.center_lines
        Center_Points = self.center_points

        for center in centers:
            [center_point] = Center_Points[center]
            center_point.set_xdata([])
            center_point.set_ydata([])
            center_point.set_label('')

            for [center_lines] in Center_Lines[center]:
                center_lines.set_xdata([])
                center_lines.set_ydata([])
                center_lines.set_label('')
            

        [triangle_lines] = self.triangle_lines
        triangle_lines.set_xdata([])
        triangle_lines.set_ydata([])

        self.Draw_Triangle()


        self.center_draw_flags = center_draw_flags

        try:
            ax.get_legend().remove()
        except AttributeError:
            pass



    def Create_Random_Button(self):

        fig = self.fig
        ax = fig.add_axes([0.1, 0.40, 0.125, 0.075])
        randomize_button = Button(ax, 'Randomize')
        randomize_button.label.set_fontsize(20)

        randomize_button.on_clicked(self.random_button_click)

        self.randomize_button = randomize_button


    def random_button_click(self, event):

        A = np.array([random(), random()])
        B = np.array([random(), random()])
        C = np.array([random(), random()])



        self.triangle = Triangle(A, B, C)

        #Update the triangle
        self.Update_Triangle()

        #Update the centers
        self.Update_Centers()


    def centroid_button_click(self, event):

        triangle = self.triangle
        ax = self.triangle_axis

        center_lines = self.center_lines['Centroid']
        [center_point] = self.center_points['Centroid']

        center_draw_flags = self.center_draw_flags

        center_draw_flags['Centroid'] = (center_draw_flags['Centroid'] + 1) % 4

        #0 -> No draw, 1 -> Draw 1 line, 2 Draw center and lines, 3 -> Draw center only
        if center_draw_flags['Centroid'] == 0:
            for [center_line] in center_lines:
                center_line.set_xdata([])
                center_line.set_ydata([])
            center_point.set_xdata([])
            center_point.set_ydata([])
            center_point.set_label('')

            handles, labels = ax.get_legend_handles_labels()

            if len(labels) > 0:
                ax.legend(bbox_to_anchor=(1.45, 1.00), fontsize = 18)
            else:
                ax.get_legend().remove()

        elif center_draw_flags['Centroid'] == 1:
            
            X, Y = triangle.Generate_Medians()
            for x, y, [center_line] in zip(X, Y, center_lines):
                center_line.set_xdata([x])
                center_line.set_ydata([y])
                center_line.set_label('Median')
                #Only draw the first
                break
            
            ax.legend(bbox_to_anchor=(1.45, 1.00), fontsize = 18)
            
            

        elif center_draw_flags['Centroid'] == 2:

            x, y = triangle.Generate_Centroid()
            center_point.set_xdata([x])
            center_point.set_ydata([y])
            center_point.set_label('Centroid')

            X, Y = triangle.Generate_Medians()

            for x, y, [center_line] in zip(X, Y, center_lines):
                center_line.set_xdata([x])
                center_line.set_ydata([y])


            ax.legend(bbox_to_anchor=(1.45, 1.00), fontsize = 18)

        elif center_draw_flags['Centroid'] == 3:


            for [center_line] in center_lines:
                center_line.set_xdata([])
                center_line.set_ydata([])
                center_line.set_label('')
            ax.legend(bbox_to_anchor=(1.45, 1.00), fontsize = 18)




    def incenter_button_click(self, event):

        triangle = self.triangle
        ax = self.triangle_axis

        [inscribed] = self.inscribed

        center_draw_flags = self.center_draw_flags

        center_lines = self.center_lines['Incenter']
        [center_point] = self.center_points['Incenter']

        center_draw_flags['Incenter'] = (center_draw_flags['Incenter'] + 1) % 4

        #0 -> No draw, 1 -> Draw 1 line, 2 Draw center and lines, 3 -> Draw center only
        if center_draw_flags['Incenter'] == 0:
            for [center_line] in center_lines:
                center_line.set_xdata([])
                center_line.set_ydata([])
            center_point.set_xdata([])
            center_point.set_ydata([])
            center_point.set_label('')

            handles, labels = ax.get_legend_handles_labels()

            if len(labels) > 0:
                ax.legend(bbox_to_anchor=(1.45, 1.00), fontsize = 18)
            else:
                ax.get_legend().remove()

        elif center_draw_flags['Incenter'] == 1:

            X, Y = triangle.Generate_AngleBisectors()
            for x, y, [center_line] in zip(X, Y, center_lines):
                center_line.set_xdata([x])
                center_line.set_ydata([y])
                center_line.set_label('Angle\nBisector')
                break
            ax.legend(bbox_to_anchor=(1.45, 1.00), fontsize = 18)
            

        elif center_draw_flags['Incenter'] == 2:

            x, y = triangle.Generate_Incenter()
            center_point.set_xdata([x])
            center_point.set_ydata([y])
            center_point.set_label('Incenter')

            X, Y = triangle.Generate_AngleBisectors()
            for x, y, [center_line] in zip(X, Y, center_lines):
                center_line.set_xdata([x])
                center_line.set_ydata([y])

            x, y = triangle.Generate_Inscribed()
            inscribed.set_xdata([x])
            inscribed.set_ydata([y])
                

            ax.legend(bbox_to_anchor=(1.45, 1.00), fontsize = 18)

        elif center_draw_flags['Incenter'] == 3:


            for [center_line] in center_lines:
                center_line.set_xdata([])
                center_line.set_ydata([])
                center_line.set_label('')

            inscribed.set_xdata([])
            inscribed.set_ydata([])

            ax.legend(bbox_to_anchor=(1.45, 1.00), fontsize = 18)



    def circumcenter_button_click(self, event):

        triangle = self.triangle
        ax = self.triangle_axis

        [circumscribed] = self.circumscribed

        center_draw_flags = self.center_draw_flags

        center_lines = self.center_lines['Circumcenter']
        [center_point] = self.center_points['Circumcenter']

        center_draw_flags['Circumcenter'] = (center_draw_flags['Circumcenter'] + 1) % 4

        #0 -> No draw, 1 -> Draw 1 line, 2 Draw center and lines, 3 -> Draw center only
        if center_draw_flags['Circumcenter'] == 0:
            for [center_line] in center_lines:
                center_line.set_xdata([])
                center_line.set_ydata([])
            center_point.set_xdata([])
            center_point.set_ydata([])
            center_point.set_label('')

            handles, labels = ax.get_legend_handles_labels()

            if len(labels) > 0:
                ax.legend(bbox_to_anchor=(1.45, 1.00), fontsize = 18)
            else:
                ax.get_legend().remove()

        elif center_draw_flags['Circumcenter'] == 1:

            X, Y = triangle.Generate_PerpendicularBisectors()
            for x, y, [center_line] in zip(X, Y, center_lines):
                center_line.set_xdata([x])
                center_line.set_ydata([y])
                center_line.set_label('Perpendicular\nBisector')
                break
            ax.legend(bbox_to_anchor=(1.45, 1.00), fontsize = 18)
            

        elif center_draw_flags['Circumcenter'] == 2:

            x, y = triangle.Generate_Circumcenter()
            center_point.set_xdata([x])
            center_point.set_ydata([y])
            center_point.set_label('Circumcenter')

            X, Y = triangle.Generate_PerpendicularBisectors()
            for x, y, [center_line] in zip(X, Y, center_lines):
                center_line.set_xdata([x])
                center_line.set_ydata([y])

            x, y = triangle.Generate_Circumscribed()
            circumscribed.set_xdata([x])
            circumscribed.set_ydata([y])
                

            ax.legend(bbox_to_anchor=(1.45, 1.00), fontsize = 18)

        elif center_draw_flags['Circumcenter'] == 3:


            for [center_line] in center_lines:
                center_line.set_xdata([])
                center_line.set_ydata([])
                center_line.set_label('')

            circumscribed.set_xdata([])
            circumscribed.set_ydata([])
            
            ax.legend(bbox_to_anchor=(1.45, 1.00), fontsize = 18)




    def orthocenter_button_click(self, event):

        triangle = self.triangle
        ax = self.triangle_axis

        center_draw_flags = self.center_draw_flags

        center_lines = self.center_lines['Orthocenter']
        [center_point] = self.center_points['Orthocenter']

        center_draw_flags['Orthocenter'] = (center_draw_flags['Orthocenter'] + 1) % 4


        #0 -> No draw, 1 -> Draw 1 line, 2 Draw center and lines, 3 -> Draw center only
        if center_draw_flags['Orthocenter'] == 0:
            for [center_line] in center_lines:
                center_line.set_xdata([])
                center_line.set_ydata([])
            center_point.set_xdata([])
            center_point.set_ydata([])
            center_point.set_label('')

            handles, labels = ax.get_legend_handles_labels()

            if len(labels) > 0:
                ax.legend(bbox_to_anchor=(1.45, 1.00), fontsize = 18)
            else:
                ax.get_legend().remove()


        elif center_draw_flags['Orthocenter'] == 1:

            X, Y = triangle.Generate_Altitudes()
            for x, y, [center_line] in zip(X, Y, center_lines):
                center_line.set_xdata([x])
                center_line.set_ydata([y])
                center_line.set_label('Altitude')
                break
            ax.legend(bbox_to_anchor=(1.45, 1.00), fontsize = 18)
            

        elif center_draw_flags['Orthocenter'] == 2:

            x, y = triangle.Generate_Orthocenter()
            center_point.set_xdata([x])
            center_point.set_ydata([y])
            center_point.set_label('Orthocenter')

            X, Y = triangle.Generate_Altitudes()
            for x, y, [center_line] in zip(X, Y, center_lines):
                center_line.set_xdata([x])
                center_line.set_ydata([y])
                

            ax.legend(bbox_to_anchor=(1.45, 1.00), fontsize = 18)

        elif center_draw_flags['Orthocenter'] == 3:


            for [center_line] in center_lines:
                center_line.set_xdata([])
                center_line.set_ydata([])
                center_line.set_label('')

            ax.legend(bbox_to_anchor=(1.45, 1.00), fontsize = 18)

        


    def mouse_click_callback(self, event):
        '''Whenever the mouse is clicked.'''

        #If the click did not occur within the axis, who cares
        if event.inaxes is None:
            return

        #If button is not a left click (I think)
        elif event.button != 1:
            return

        else:
            self.vind = self.get_ind_under_point(event)


    def mouse_release_callback(self, event):
        '''When the mouse is released, reset vind to None'''

        #This only happens on left clicks
        if event.button != 1:
            return
        else:
            self.vind = None


    def get_ind_under_point(self, event):

        ax = self.triangle_axis

        #Need to convert event.x and event.y coordinates (which are in strange coordinates)
        #to the local coordinates
        t = ax.transData.inverted()
        tinv = ax.transData
        click_coords = t.transform([event.x,event.y])

        #Grab the vertices of the triangle
        vertices = self.triangle.Vertices

        #Create three line segments, connecting the click_coords to each vertex and find the
        #length of each line
        d = [LineSegment(v, click_coords).Length() for v in vertices]

        #Find the index of the vertex whose distance to the mouse click point is smallest
        ind = d.index(min(d))


        #If the distance between the vertex and the mouse click is less than epsilon,
        #then update the vind attribute accordingly. Otherwise update it to None.
        if d[ind] <= self.epsilon:
            return ind

        else:
            return None



    def mouse_movement_callback(self, event):
        '''When the mouse moves'''

        #The mouse movement only can only have an effect if the button is clicked
        #inside the axis and vind != None
        vind = self.vind
        if vind is None or event.button != 1 or event.inaxes is None:
            return

        else:

            ax = self.triangle_axis
            fig = self.fig

            t = ax.transData.inverted()
            tinv = ax.transData
            x, y = t.transform([event.x,event.y])


            vertices = self.triangle.Vertices
            vertices[vind] = np.array([x, y])
            A, B, C = vertices
            self.triangle = Triangle(A, B, C)

            #Update the triangle
            self.Update_Triangle()

            #Update the centers
            self.Update_Centers()

            fig.canvas.draw_idle()


    def Update_Triangle(self):

        ax = self.triangle_axis
        [line] = self.triangle_lines
        triangle = self.triangle

        X, Y = triangle.Generate_Triangle()
        line.set_xdata(X)
        line.set_ydata(Y)



    def Update_Centers(self):

        triangle = self.triangle
        [inscribed] = self.inscribed
        [circumscribed] = self.circumscribed

        center_draw_flags = self.center_draw_flags

        Center_Lines = self.center_lines
        Center_Point = self.center_points

        for center in Center_Lines:
            [center_point] = Center_Point[center]
            center_lines = Center_Lines[center]

            if center_draw_flags[center] == 1:

                #Update both the lines and the center
                if center == 'Centroid':

                    X, Y = triangle.Generate_Medians()
                    for x, y, [center_line] in zip(X, Y, center_lines):
                        center_line.set_xdata([x])
                        center_line.set_ydata([y])
                        break

                elif center == 'Incenter':

                    X, Y = triangle.Generate_AngleBisectors()
                    for x, y, [center_line] in zip(X, Y, center_lines):
                        center_line.set_xdata([x])
                        center_line.set_ydata([y])
                        break

                elif center == 'Circumcenter':

                    X, Y = triangle.Generate_PerpendicularBisectors()
                    for x, y, [center_line] in zip(X, Y, center_lines):
                        center_line.set_xdata([x])
                        center_line.set_ydata([y])
                        break

                elif center == 'Orthocenter':


                    X, Y = triangle.Generate_Altitudes()
                    for x, y, [center_line] in zip(X, Y, center_lines):
                        center_line.set_xdata([x])
                        center_line.set_ydata([y])
                        break

                
            elif center_draw_flags[center] == 2:
                
                #Update both the lines and the center
                if center == 'Centroid':

                    x, y = triangle.Generate_Centroid()
                    center_point.set_xdata([x])
                    center_point.set_ydata([y])

                    X, Y = triangle.Generate_Medians()
                    for x, y, [center_line] in zip(X, Y, center_lines):
                        center_line.set_xdata([x])
                        center_line.set_ydata([y])

                elif center == 'Incenter':

                    x, y = triangle.Generate_Incenter()
                    center_point.set_xdata([x])
                    center_point.set_ydata([y])

                    X, Y = triangle.Generate_AngleBisectors()
                    for x, y, [center_line] in zip(X, Y, center_lines):
                        center_line.set_xdata([x])
                        center_line.set_ydata([y])

                    x, y = triangle.Generate_Inscribed()
                    inscribed.set_xdata([x])
                    inscribed.set_ydata([y])

                elif center == 'Circumcenter':

                    x, y = triangle.Generate_Circumcenter()
                    center_point.set_xdata([x])
                    center_point.set_ydata([y])

                    X, Y = triangle.Generate_PerpendicularBisectors()
                    for x, y, [center_line] in zip(X, Y, center_lines):
                        center_line.set_xdata([x])
                        center_line.set_ydata([y])

                    x, y = triangle.Generate_Circumscribed()
                    circumscribed.set_xdata([x])
                    circumscribed.set_ydata([y])

                elif center == 'Orthocenter':

                    x, y = triangle.Generate_Orthocenter()
                    center_point.set_xdata([x])
                    center_point.set_ydata([y])

                    X, Y = triangle.Generate_Altitudes()
                    for x, y, [center_line] in zip(X, Y, center_lines):
                        center_line.set_xdata([x])
                        center_line.set_ydata([y])


            elif center_draw_flags[center] == 3:

                #Update only the center
                if center == 'Centroid':

                    x, y = triangle.Generate_Centroid()
                    center_point.set_xdata([x])
                    center_point.set_ydata([y])


                elif center == 'Incenter':

                    x, y = triangle.Generate_Incenter()
                    center_point.set_xdata([x])
                    center_point.set_ydata([y])


                elif center == 'Circumcenter':

                    x, y = triangle.Generate_Circumcenter()
                    center_point.set_xdata([x])
                    center_point.set_ydata([y])


                elif center == 'Orthocenter':

                    x, y = triangle.Generate_Orthocenter()
                    center_point.set_xdata([x])
                    center_point.set_ydata([y])



                    

            



if __name__ == '__main__':


    TV = TriangleViewer()
