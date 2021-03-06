#!/usr/bin/env python

import anim_solvers.stick_figure as sf
import anim_solvers.myarrows as arrow
import numpy as np
import matplotlib.pylab as plt

class Earth(object):
    """ draw Earth and add embelishments to
        illustrate basic concepts """

    def __init__(self, latitude=40, axial_tilt=-23.5):

        self.lat = latitude

        # note that angles are measured counterclockwise from the +x
        # axis.  making it negative gives us the summer solstice
        self.tilt = axial_tilt

        # scalings for the person and earth
        self.L = 1.5
        self.R = 10

        # location of Earth
        self.x0 = 0.0
        self.y0 = 0.0

    def draw_earth(self):

        # draw a circle
        theta = np.radians(np.arange(0,361))
        plt.plot(self.x0 + self.R*np.cos(theta),
                 self.y0 + self.R*np.sin(theta), c="b")


    def draw_day_night(self):

        theta_half = np.radians(np.arange(90,271))
        plt.fill(list(self.x0 + self.R*np.cos(theta_half)) +
                 [self.x0 +self.R*np.cos(theta_half[0])],
                 list(self.y0 + self.R*np.sin(theta_half)) +
                 [self.y0 +self.R*np.sin(theta_half[0])], "0.75",
                 zorder=-1)


    def draw_ecliptic(self):

        L = 5.0

        plt.plot([self.x0 -1.2*self.R, self.x0 + L*self.R],
                 [self.y0, self.y0], ls=":", color="k")

        plt.plot([self.x0, self.x0],
                 [self.y0-self.R, self.y0+self.R], ls=":", color="k")

        plt.text(self.x0 + L*self.R, self.y0 + 0.1*self.R,
                 "ecliptic", horizontalalignment="right")


    def draw_rot_axis(self):

        overhang = 1.2

        ps = (self.x0, self.y0 - overhang*self.R)
        pe = (self.x0, self.y0 + overhang*self.R)

        ts = sf._rotate(ps, (self.x0, self.y0), np.radians(self.tilt))
        te = sf._rotate(pe, (self.x0, self.y0), np.radians(self.tilt))

        plt.plot([ts[0], te[0]], [ts[1], te[1]], color="b")


        a = arrow.ArcArrow((0, 0), 0.5*self.R, 
                           theta_start=90+self.tilt, theta_end=90.0)
        a.draw(color="b")

        mid = 0.5*(90 + self.tilt + 90)
        plt.text(0.51*self.R*np.cos(np.radians(mid)),
                 0.51*self.R*np.sin(np.radians(mid)), 
                 r"$\alpha$", color="b", horizontalalignment="left")


    def draw_parallel(self, l, color="k", ls="-", label=None):
        """ draw a line of latitude """

        # working in Earth coordinates
        # find the (x, y) of the parallel start and end
        xs = self.x0 - self.R*np.cos(np.radians(l))
        ys = self.y0 + self.R*np.sin(np.radians(l))
        
        xe = self.x0 + self.R*np.cos(np.radians(l))
        ye = self.y0 + self.R*np.sin(np.radians(l))
        

        # since we are tilted, the actual angle in the drawing
        # (from +x) is l + tilt
        angle = self.tilt

        # transform the points into the rotated frame
        ts = sf._rotate((xs, ys), (self.x0, self.y0), np.radians(angle))
        te = sf._rotate((xe, ye), (self.x0, self.y0), np.radians(angle))

        plt.plot([ts[0], te[0]], [ts[1], te[1]], color=color, ls=ls)

        if label is not None:
            if l > 0:
                va = "bottom"
            elif l == 0:
                va = "center"
            else:
                va = "top"

            plt.text(ts[0]-0.01*self.R, ts[1], label, 
                     horizontalalignment="right", verticalalignment=va, color=color)


    def draw_equator(self):
        self.draw_parallel(0, color="b", label="equator")


    def draw_sun(self):
        plt.scatter([self.x0 + 4.5*self.R], [self.y0], 
                    s=2000, marker=(16,1), zorder=100, color="k")
        plt.scatter([self.x0 + 4.5*self.R], [self.y0], 
                    s=1900, marker=(16,1), zorder=100, color="#FFFF00")

    def draw_tropics(self):
        self.draw_parallel(np.abs(self.tilt), color="g", ls="--", label="tropic of cancer")
        self.draw_parallel(-np.abs(self.tilt), color="g", ls="--", label="tropic of capricorn")


    def draw_arctic_circles(self):
        self.draw_parallel(90-np.abs(self.tilt), color="g", ls="--", label="arctic circle")
        self.draw_parallel(-90+np.abs(self.tilt), color="g", ls="--", label="antarctic circle")


    def draw_my_latitude(self):

        angle = self.lat + self.tilt

        center = ( (self.R + 0.5*self.L)*np.cos(np.radians(angle)),
                   (self.R + 0.5*self.L)*np.sin(np.radians(angle)) )

        sf.draw_person(center, self.L, np.radians(angle - 90), color="r")

        equator = 0 + self.tilt

        plt.plot([self.x0, self.R*np.cos(np.radians(angle))],
                 [self.y0, self.R*np.sin(np.radians(angle))], color="r", ls="-")

        a = arrow.ArcArrow((self.x0, self.y0), 0.5*self.R, theta_start=equator, theta_end=angle)
        a.draw(color="r")

        mid = 0.5*(equator + angle)
        plt.text(0.51*self.R*np.cos(np.radians(mid)),
                 0.51*self.R*np.sin(np.radians(mid)), r"$l$", color="r", horizontalalignment="left")


    def draw_zenith(self):

        angle = self.lat + self.tilt

        print("here")
        zenith = 3.0*self.R
        plt.plot([self.x0, zenith*np.cos(np.radians(angle))],
                 [self.y0, zenith*np.sin(np.radians(angle))], color="r", ls=":")

        plt.text(zenith*np.cos(np.radians(angle)),
                 zenith*np.sin(np.radians(angle)), "zenith", color="r",
                 horizontalalignment="left")


    def draw_horizon(self):
        angle = self.tilt + self.lat

        sc = ( self.x0 + self.R*np.cos(np.radians(angle)),
               self.y0 + self.R*np.sin(np.radians(angle)) )

        ps = (-0.75*self.R, 0)
        pe = (0.75*self.R, 0)

        ts = sf._rotate(ps, (0, 0), np.radians(90+angle))
        te = sf._rotate(pe, (0, 0), np.radians(90+angle))

        plt.plot([sc[0]+ts[0], sc[0]+te[0]], [sc[1]+ts[1], sc[1]+te[1]], color="c")
        plt.text(sc[0]+ts[0], sc[1]+ts[1], "local horizon", 
                 horizontalalignment="left",
                 verticalalignment="top",
                 rotation=270+angle, color="c")             



class Scene(object):
    """ a container to hold the sequence of function calls we will do to
        compose the scene.  This way we can incrementally add to the
        figure """

    def __init__(self, other, xlim=None, ylim=None):
        self.other = other
        self.funcs = []
        self.xlim = xlim
        self.ylim = ylim

    def addto(self, f):
        self.funcs.append(f)

    def draw(self, description=None, ofile="test.png"):

        plt.clf()

        for f in self.funcs:
            f()

        plt.axis("off")

        ax = plt.gca()
        ax.set_aspect("equal", "datalim")

        f = plt.gcf()
        f.set_size_inches(12.8, 7.2)

        if description is not None:
            plt.text(0.025, 0.05, description, transform=f.transFigure)

        if self.xlim is not None:
            plt.xlim(*self.xlim)

        if self.ylim is not None:
            plt.ylim(*self.ylim)

        plt.subplots_adjust(left=0, bottom=0, right=1, top=1, wspace=0, hspace=0)

        # dpi = 100 for 720p, 150 for 1080p
        plt.savefig(ofile, dpi=150)


def doit():

    e = Earth(latitude=42)

    sc = Scene(e, xlim=(-2*e.R, 5*e.R), ylim=(-2*e.R, 2*e.R))

    n = 0
    sc.addto(e.draw_earth)
    sc.addto(e.draw_ecliptic)
    sc.addto(e.draw_sun)
    sc.draw(ofile="earth_{:02d}".format(n), 
            description="Earth and the ecliptic:\n" +
            "the ecliptic is the orbital plane, connecting the Earth and the Sun")

    n += 1
    sc.addto(e.draw_day_night)
    sc.draw(ofile="earth_{:02d}".format(n), 
            description="the day/night line:\n" +
            "night is the hemisphere pointed away from the Sun")

    n += 1
    sc.addto(e.draw_rot_axis)
    sc.draw(ofile="earth_{:02d}".format(n), 
            description="Earth's axial tilt:\n" +
            r"Earth's rotation axis is tilted and angle $\alpha = 23.5^\circ$ with respect to the ecliptic")

    n += 1
    sc.addto(e.draw_equator)
    sc.draw(ofile="earth_{:02d}".format(n), 
            description="Earth's equator:\n" +
            "the equator is perpendicular to the rotation axis")

    n += 1
    sc.draw(ofile="earth_{:02d}".format(n), 
            description="the Sun:\n" +
            "the Sun is on the ecliptic (not shown to scale)\n" +
            "here Earth's North Pole is maximally pointed toward the Sun -- this is the day of the summer solstice")


    n += 1
    sc.addto(e.draw_my_latitude)
    sc.draw(ofile="earth_{:02d}".format(n), 
            description="latitude on Earth:\n" + 
            r"latitude is just the angle above or below the equator.  Here is an observer at a latitude $l$")

    n += 1
    sc.addto(e.draw_zenith)
    sc.draw(ofile="earth_{:02d}".format(n), 
            description="your zenith:\n" + 
            "down is the direction connecting you to the center of the Earth (the direction gravity points)\n" +
            "up is opposite down -- here the zenith is shown as the point directly above us")

    n += 1
    sc.addto(e.draw_tropics)
    sc.draw(ofile="earth_{:02d}".format(n), 
            description="the tropics:\n" + 
            r"the tropic lines are +/- $\alpha$ in latitude -- note that the Sun is directly overhead for an observer on the Tropic of Cancer on the summer solstice")

    n += 1
    sc.addto(e.draw_arctic_circles)
    sc.draw(ofile="earth_{:02d}".format(n), 
            description="the arctic and antarctic circles:\n" +
            "on the summer solstice the Sun never sets between the arctic circle and North Pole -- note how everything is in daylight at these high latitudes\n" +
            "the opposite is true between the antarctic circle and the South Pole -- the Sun is never above the horizon (always night)\n" +
            r"these latitudes are just +/- $(90^\circ - \alpha)$")

    n += 1
    sc.addto(e.draw_horizon)
    sc.draw(ofile="earth_{:02d}".format(n), 
            description="horizon:\n" +
            "your local horizon is tangent to the surface of the Earth where you are standing")

    sc.draw()




if __name__ == "__main__":
    doit()
