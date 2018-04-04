# Smith, Mitchel J.R.
# 1000-799-110
# 2018-02-27

#----------------------------------------------------------------------
# This code was originally created by Prof. Farhad Kamangar.
# It has been somewhat modified and updated by Brian A. Dalio for use
# in CSE 4303 / CSE 5365 in the 2018 Spring semester.

#----------------------------------------------------------------------
class cl_world :
    def __init__( self, objects = [], canvases = [] ) :
        self.objects = objects
        self.canvases = canvases

    def add_canvas( self, canvas ) :
        self.canvases.append( canvas )
        canvas.world = self

    def create_graphic_objects( self, canvas, lines ) :

        for line in lines:
            if line[0] == 's':
                type,vx_min,vy_min,vx_max,vy_max = line.split()
            if line[0] == 'w':
                type,wx_min,wy_min,wx_max,wy_max = line.split()

        width = float(canvas.cget( "width" ))
        height = float(canvas.cget( "height" ))

        vx_min = float(vx_min)
        vy_min = float(vy_min)
        vx_max = float(vx_max)
        vy_max = float(vy_max)
        wx_min = float(wx_min)
        wy_min = float(wy_min)
        wx_max = float(wx_max)
        wy_max = float(wy_max)

        vx_min = vx_min * width
        vy_min = vy_min * height
        vx_max = vx_max * width
        vy_max = vy_max * height

        fx = wx_min * -1
        fy = wy_min * -1
        sx = ((vx_max - vx_min) / (wx_max - wx_min))
        sy = ((vy_max - vy_min) / (wy_max - wy_min))
        x = ((fx * sx) + vx_min)
        y = ((fy * sy) + vy_min)

        canvas.create_line(vx_min, vy_min, vx_min, vy_max, vx_max, vy_max, vx_max, vy_min, vx_min, vy_min)

        for line in lines:
            if line[0] == 'f':
                type, va, vb, vc = line.split()
                v1 = float(va) - 1
                v2 = float(vb) - 1
                v3 = float(vc) - 1

                vertices = []
                i = 0
                for l in lines:
                    if i == v1:
                        vertices.append(l)
                    i += 1

                i = 0
                for l in lines:
                    if i == v2:
                        vertices.append(l)
                    i += 1

                i = 0
                for l in lines:
                    if i == v3:
                        vertices.append(l)
                    i += 1

                print(vertices)
                print()

                x1 = 0
                x2 = 0
                x3 = 0
                y1 = 0
                y2 = 0
                y3 = 0

                j = 1
                for v in vertices:
                    type, m, n, z = v.split()
                    if j == 1:
                        x1 = m
                        y1 = n
                    if j == 2:
                        x2 = m
                        y2 = n
                    if j == 3:
                        x3 = m
                        y3 = n
                    j += 1

                x1 = float(x1)
                y1 = float(y1)
                x2 = float(x2)
                y2 = float(y2)
                x3 = float(x3)
                y3 = float(y3)

                xa = sx * x1 + x
                ya = sy * y1 + y
                xb = sx * x2 + x
                yb = sy * y2 + y
                xc = sx * x3 + x
                yc = sy * y3 + y

                canvas.create_line(xa, ya, xb, yb, xc, yc, xa, ya)

    def redisplay( self, canvas, event ) :
        if self.objects :
            canvas.coords(self.objects[ 0 ], 0, 0, event.width, event.height )
            canvas.coords(self.objects[ 1 ], event.width, 0, 0, event.height )
            canvas.coords(self.objects[ 2 ],
                int( 0.25 * int( event.width ) ),
                int( 0.25 * int( event.height ) ),
                int( 0.75 * int( event.width ) ),
                int( 0.75 * int( event.height ) ) )

#----------------------------------------------------------------------
