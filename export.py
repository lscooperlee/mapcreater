
import random

class MapExporter:

    def __init__(self, noise_rate=0.02, ang_noise_dir=0.52, dist_noise_dir=0.48, dist_rate=50, total_scan=500):

        self.noise_rate=noise_rate
        self.ang_noise_dir=ang_noise_dir
        self.dist_noise_dir=dist_noise_dir
        self.dist_rate=dist_rate
        self.total_scan=total_scan

        self.scan_id=0
    
    def randomise(self, point):
        newx=(1+self.dist_noise_dir-0.5+random.random()*self.noise_rate)*point[0]
        newy=(1+self.dist_noise_dir-0.5+random.random()*self.noise_rate)*point[1]
        newa=(1+self.ang_noise_dir-0.5+random.random()*self.noise_rate)*point[2]

        return (newx,newy,newa)

    def export_info(self):
        info="""LaserOdometryLog
#Created by MapCreater, a virtual map generator
version: 1
noise_rate: {0.noise_rate}
angle_noise_direction: {0.ang_noise_dir}
distance_noise_direction: {0.dist_noise_dir}
distance_rate: {0.dist_rate}
total_scan: {0.total_scan}""".format(self)

        return info

    def export_head(self, ry,rx,ra):
        self.scan_id+=1

        #ra is Qt angle, x axis is 0 degree. y axis is 90, but for Aria log, the y axis is 0, and x ais is 90
        
        ra=ra if ra < 180 else ra-360
        ra=ra if ra > -180 else ra+360
        a=90-ra if 90 -ra < 180 else -90 - ra

        head="""
scan1Id: {0}
time: 0.00
velocities: 0.00 0.00 0.00
robot: 0.00 0.00 0.00
robotGlobal: {1:.0f} {2:.0f} {3:.2f}""".format(self.scan_id, ry*self.dist_rate,rx*self.dist_rate,a)

        return head

    def export_scan(self, scanlist):
        scan="""
scan1:"""
        for i in scanlist:
            scan+=" {:.0f} {:.0f} ".format(i[0]*self.dist_rate,i[1]*self.dist_rate)
        
        return scan

    def export(self, poslist, mapimage, outputfile):
        pass

