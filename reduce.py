class Reduce:
    def __init__(self, dotsArr, amp):
        self.da = dotsArr
        self.amp = amp

    def getDebugDots(self):
        out = []
        for i in range(len(self.da)-1):
            d1 = self.da[i]
            d2 = self.da[i+1]

            k, b, f = self.getLineParams(d1, d2)

            kPer1, bPer1, fPer1 = self.getPerpendicular(k, b, f, d1)
            kPer2, bPer2, fPer2 = self.getPerpendicular(k, b, f, d2)

            kPar, bPar1, bPar2, fPar = self.getParallel(k, b, f)

            if f:
                # kPer1 bPer1 <> kPar bPar1
                x1 = (bPer1 - bPar1) / (kPar - kPer1)
                # kPer1 bPer1 <> kPar bPar2
                x2 = (bPer1 - bPar2) / (kPar - kPer1)
                # kPer2 bPer2 <> kPar bPar1
                x3 = (bPer2 - bPar1) / (kPar - kPer2)
                # kPer2 bPer2 <> kPar bPar2
                x4 = (bPer2 - bPar2) / (kPar - kPer2)

                y1 = kPer1*x1 + bPer1
                y2 = kPer1*x2 + bPer1
                y3 = kPer2*x3 + bPer2
                y4 = kPer2*x4 + bPer2

                out.append(
                    [
                        [x1, y1],
                        [x2, y2],
                        [x4, y4],
                        [x3, y3]
                    ]
                )

        return out

    def reduce(self):
        i = 0

        while i < len(self.da)-2:
            d1 = self.da[i]
            d2 = self.da[i+1]
            d3 = self.da[i+2]

            k, b, f = self.getLineParams(d1, d3)

            kPer1, bPer1, fPer1 = self.getPerpendicular(k, b, f, d1)
            kPer2, bPer2, fPer2 = self.getPerpendicular(k, b, f, d3)

            kPar, bPar1, bPar2, fPar = self.getParallel(k, b, f)

            onParallels = False
            onPerpendiculars = False

            if f:
                y1 = kPar*d2[0] + bPar1
                y2 = kPar*d2[0] + bPar2
 
                Par1 = d2[1] < y1
                Par2 = d2[1] > y2

                onParallels = Par1 and Par2
            else:
                x1 = d2[0] > d1[0]-self.amp 
                x2 = d2[0] < d1[0]+self.amp 

                onParallels = x1 and x2

            if fPer1:
                y1 = kPer1 * d2[0] + bPer1
                y2 = kPer2 * d2[0] + bPer2

                Per1 = d2[1] < max(y1, y2)
                Per2 = d2[1] > min(y1, y2)

                onPerpendiculars = Per1 and Per2
            else:
                y1 = d2[1] > d1[1]-self.amp 
                y2 = d2[1] < d1[1]+self.amp 

                onPerpendiculars = y1 and y2

            if onParallels and onPerpendiculars:
                self.da.pop(i+1)
            else:
                i += 1

    def getLineParams(self, d1=[], d2=[]):
        dx = d2[0] - d1[0]
        dy = d2[1] - d1[1]

        if dx == 0:
            return 0, d1[0], False
        
        k = dy / dx
        b = d1[1] - k*d1[0]

        return k, b, True

    def getPerpendicular(self, k=0, b=0, flag=True, dot=[]):
        if flag:
            if k == 0:
                return 0, dot[0],  False
            else:
                kp = -1 / k
                bp = dot[0]/k + dot[1]

                return kp, bp, flag
        else:
            return 0, dot[1],  True

    def getParallel(self, k, b, flag):
        if flag:
            x = 0
            y = b

            from math import atan
            from math import sin
            from math import cos
            from math import pi

            a = atan(k) + pi/2

            xp = x + self.amp * cos(a)
            yp = y + self.amp * sin(a)

            bp = yp - k * xp

            abp = abs(b-bp)

            return k, b+abp, b-abp, flag
        else:
            return k, b+self.amp, b-self.amp, flag
