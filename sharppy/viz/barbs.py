import numpy as np
from PySide import QtGui, QtCore
import sharppy.sharptab as tab
from sharppy.sharptab.constants import *

## routine written by Kelton Halbert
## keltonhalbert@ou.edu


def drawBarb( qp, origin_x, origin_y, u, v, color='#FFFFFF' ):
    pen = QtGui.QPen(QtGui.QColor(color), 1, QtCore.Qt.SolidLine)
    pen.setWidthF(1.75)
    qp.setPen(pen)
    wnd = np.ceil( tab.utils.mag(u, v) )
    ## check if there are any 50kt triangles needed
    if wnd < 5.:
        point = QtCore.QPoint( origin_x, origin_y )
        qp.drawEllipse(point, 3, 3)
    else:
        ## turn the vector into a normal vector
        u_norm = (u / wnd)
        v_norm = (v / wnd)
        ## get the end point of the vector. The scalar multiple is to give it length
        end_x = origin_x - u_norm * 25
        end_y = origin_y + v_norm * 25
        qp.drawLine(origin_x, origin_y, end_x, end_y)
        num_flag_barbs = int( wnd / 50. )
        num_full_barbs = int( wnd / 10. ) % 5
        num_half_barbs = int( wnd / 5. ) % 2
        ## draw the flag barbs
        for i in range(num_flag_barbs):
            ## use this as a linear offset from the previous barb,
            ## starting at the end
            offset1 = 4. * i
            offset2 = 4. * (i+1)
            ## calculate the u nd v offset
            offset_x1 = u_norm * offset1
            offset_x2 = u_norm * offset2
            offset_y1 = v_norm * offset1
            offset_y2 = v_norm * offset2
            ## starting from the end of the wind barb, work back
            ## towards the origin in increments of the offset
            barbx_start = end_x + offset_x1
            flagx_start = end_x + offset_x2
            barby_start = end_y - offset_y1
            flagy_start = end_y - offset_y2
            ## then draw outward perpendicular to the wind barb
            barbx_end = barbx_start - v_norm * 10
            barby_end = barby_start - u_norm * 10
            ## draw the barb
            qp.drawLine(barbx_start, barby_start, barbx_end, barby_end)
            qp.drawLine(flagx_start, flagy_start, barbx_end, barby_end)
        
        for i in range(num_full_barbs):
            ## use this as a linear offset from the previous barb,
            ## starting at the end
            if num_flag_barbs > 0:
                offset = 4. * num_flag_barbs * (i+2)
            else:
                offset = 4. * i
            ## calculate the u nd v offset
            offset_x = u_norm * offset
            offset_y = v_norm * offset
            ## starting from the end of the wind barb, work back
            ## towards the origin in increments of the offset
            barbx_start = end_x + offset_x
            barby_start = end_y - offset_y
            ## then draw outward perpendicular to the wind barb
            barbx_end = barbx_start - v_norm * 10
            barby_end = barby_start - u_norm * 10
            ## draw the barb
            qp.drawLine(barbx_start, barby_start, barbx_end, barby_end)
        
        ## draw the half barbs
        for i in range(num_half_barbs):
            ## this time we want to index from 1 so that we don't
            ## draw on top of the full barbs
            if num_flag_barbs > 0:
                i = i + 1
                offset = 4. * (num_flag_barbs + 1 + num_full_barbs)
            else:
                i = i + 1
                offset = 4. * (num_full_barbs) * i
            ## start at the increment after the last full barb
            ## get the u and v offset
            offset_x = u_norm * offset
            offset_y = v_norm * offset
            ## starting from the end of the wind barb, work back
            ## towards the origin in increments of the offset
            barbx_start = end_x + offset_x
            barby_start = end_y - offset_y
            ## then draw outward perpendicular to the wind barb
            barbx_end = barbx_start - v_norm * 5
            barby_end = barby_start - u_norm * 5
            qp.drawLine(barbx_start, barby_start, barbx_end, barby_end)