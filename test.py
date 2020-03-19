import sys
import numpy
import random
import matplotlib.image as mpimg

def read(filePath):
    src = mpimg.imread(filePath)
    image = imatrix(0, 0, 0)
    image.copymat(src)
    return image

def imageoutput(image, filePath):
    mpimg.imsave(filePath, image.sub.astype(numpy.uint8))

class error :
    def __init__(self, first, second) :
        self.first = first
        self.second = second

class imatrix:
    sub = None
    def __init__(self, row, col, mas):
        if (row*col*mas)== 0:
            self.sub = None
        else:
            self.sub = numpy.zeros((row,col,mas)).astype(numpy.intc)

    def rows(self):
        return self.sub.shape[0]

    def cols(self):
        return self.sub.shape[1]

    def copymat(self, mat):
        if mat is None:
            self.sub = None
        else:
            self.sub = numpy.copy(mat)
            if (len(self.sub.shape) == 2):
                self.sub.resize((self.sub.shape[0], self.sub.shape[1],1))

    def pixel(self,row,col,pt):
        return self.sub[(row,col,pt)]
    
    def increase(self,row,col,pt,num):
        self.sub[(row,col,pt)] += num

    def setnum(self,row,col,pt,num):
        self.sub[(row,col,pt)] = num

    def dis(self, pt,ori, num, size) :
        return numpy.sum(self.dissub(pt,ori,num,size).sub)

    def dissub(self,pt,ori,num,size):
        solu = imatrix(0, 0, 0)
        ob = imageset(self,pt.x,ori,num)
        ip_mat = pt.image.sub[pt.y:pt.y+pt.x,pt.z:pt.z+pt.x]
        op_mat = ob.image.sub[ob.y:ob.y+ob.x,ob.z:ob.z+ob.x]
        mymat = numpy.power(ip_mat-op_mat,2)
        mymat = numpy.sum(mymat,axis=2)
        mymat[size:pt.x,size:pt.x] = numpy.zeros((pt.x-size,pt.x-size))
        if (num == 0):
            mymat[size:pt.x,0:size] = numpy.zeros((pt.x-size, size))
        if (ori == 0):
            mymat[0:size,size:pt.x]= numpy.zeros((size,pt.x-size))
        solu.copymat(mymat)
        return solu
    

class imageset:
    def __init__(self,image,x,y,z):
        self.image = image
        self.x = x
        self.y = y
        self.z = z

    def copyimage(self, copyset):
        self.image.sub[self.y:self.y+self.x,self.z:self.z+self.x] = copyset.image.sub[copyset.y:copyset.y+copyset.x,copyset.z:copyset.z+copyset.x]
    
    def copyimages(self,copyset,ff):
        ori = self.image.sub[self.y:self.y+self.x,self.z:self.z+self.x]
        newset = copyset.image.sub[copyset.y:copyset.y+copyset.x,copyset.z:copyset.z+copyset.x]
        self.image.sub[self.y:self.y+self.x,self.z:self.z+self.x] = ff.sub*newset + ori - ori*ff.sub

    def pixel(self,row,col,num) :
        return self.image.pixel(row+self.y,col+self.z,num)


    def cut(self, pt, size):
        err = self.image.dissub(pt,self.y,self.z,size)
        flag = imatrix(pt.x, pt.x,1)
        for row in range(flag.rows()):
            for col in range(flag.cols()):
                flag.setnum(row,col,0,1)
            if (self.y != 0):
                mat1 =  imatrix(size,self.x,1)
                mattest = imatrix(0,0,0)
                mattest.copymat(err.sub)
                for i in range(1, self.x):
                    for j in range(size):
                        line = [j-1, j, j+1]
                        min1 = j
                        for k in range(3):
                            if (line[k] == j) or (line[k]<0) or (line[k]>=size):
                                continue
                            if mattest.pixel(line[k], i-1, 0) < mattest.pixel(min1,i-1,0): 
                                min1 = line[k]
                        mattest.increase(j,i,0,mattest.pixel(min1,i-1,0))
                        mat1.setnum(j,i,0,min1)
                min1 = 0
                for i in range(size):
                    if (mattest.pixel(i,self.x-1,0) < mattest.pixel(min1,self.x-1, 0)):
                        min1 = i
                exe = [0 for ii in range(self.x)]
                for i in range(self.x):
                    cur = self.x -1- i
                    exe[cur] = min1
                    min1 = mat1.pixel(min1,cur,0)

                for j in range(self.x):
                    for k in range(size):
                        if k>exe[j]:
                            break;
                        else:
                            flag.setnum(k,j,0,0)

            if (self.z != 0):
                mat1 =  imatrix(self.x,size,1)
                mattest = imatrix(0,0,0)
                mattest.copymat(err.sub)
                for i in range(1,self.x):
                    for j in range(size):
                        cols = [j-1,j,j+1 ]
                        min1 = j
                        for k in range(3):
                            if (cols[k] == min1) or (cols[k] < 0) or (cols[k] >= size):
                                continue
                            if mattest.pixel(i-1, cols[k], 0) < mattest.pixel(i-1, min1, 0): 
                                min1 = cols[k]
                            
                        mattest.increase(i, j, 0, mattest.pixel(i - 1, min1, 0))
                        mat1.setnum(i, j, 0, min1)

                min1 = 0
                for i in range(size):
                    if mattest.pixel(self.x - 1, i, 0) < mattest.pixel(self.x - 1,min1, 0):
                        min1 = i
                exe = [0 for ii in range(self.x)]
                for i in range(self.x):
                    cur = self.x -1 -i
                    exe[cur] = min1
                    min1 = mat1.pixel(cur, min1, 0)

                for i in range(self.x):
                    for j in range(size):
                        if j > exe[i]:
                            break
                        else:
                            flag.setnum(i, j, 0, 0)
        return flag

class image:

    def __init__(self, iimage, ix, iy, iz) : 
        self.inputImg = iimage
        self.ix = ix
        self.iy = iy
        self.iz = iz
        inum = min(iimage.rows(), iimage.cols())
        if inum < self.ix :
            self.ix = inum
        self.size = int(self.ix / 3)
        if self.size <= 0: 
            self.size = 1
        self.ip = self.ix-self.size
        i1 = 0
        i2 = 0

        if self.ix<self.iz :
            its = (self.iz - self.ix)/1.0/self.ip
            i1 = int(its)
            if its != int(its):
                i1+=1

        if self.ix<self.iy :
            its = (self.iy - self.ix)/1.0/self.ip
            i2 = int(its)
            if its != int(its) : 
                i2+=1

        self.ori = self.ix + i2 * self.ip
        self.num = self.ix + i1 * self.ip
        self.io = imatrix(self.ori, self.num,3)
        self.ir = self.inputImg.rows()
        self.ic = self.inputImg.cols()

    def  process(self): 
        pnum = 0
        pcoe = 0
        while (pcoe+self.ix <= self.ori):
            pnum += 1
            pcoe += self.ip
        for i in range(pnum):
            pcoe = i * self.ip
            pcow = 0
            while (pcow + self.ix <= self.num) :
                op =  imageset(self.io, self.ix,pcoe,pcow)
                height = self.ir - self.ix + 1
                width = self.ic-self.ix + 1
                if (pcoe == 0) and (pcow == 0):
                    coeu = random.randint(0, height-1)
                    cowu = random.randint(0, width-1)
                    pt =  imageset(self.inputImg, self.ix, coeu, cowu)
                    op.copyimage(pt)
                else:
                    perr = []
                    for j in range(height):
                        for k in range(width):
                            pic = j * width + k
                            err = self.io.dis( imageset(self.inputImg, self.ix,j, k), pcoe, pcow, self.size)
                            perr.append( error(pic, err))
                    pm = perr[0].second
                    for i in range(len(perr)):
                        if perr[i].second < pm :
                            pm = perr[i].second
                    pe = pm * 1.1
                    pa = []
                    for i in range(len(perr)):
                        if perr[i].second <= pe:
                            pa.append(i)

                    pin = pa[random.randint(0, len(pa)-1)]
                    coeu = int(pin / width)
                    cowu = int(pin % width)
                    pt =  imageset(self.inputImg, self.ix, coeu, cowu)
                    op.copyimages(pt, op.cut(pt,self.size))
                pcow += self.ip
            print(".")
                
        image_size =  imatrix(self.iy, self.iz, 3)
        for i in range(image_size.rows()):
            for j in range(image_size.cols()):
                for k in range(3):
                    image_size.setnum(i,j,k,self.io.pixel(i,j,k))
        return image_size


if __name__ == '__main__':
    input_path = ""
    output_path = ""
    texton_size = 0
    output_size = 0
    argv = sys.argv
    for i in range(len(argv)):
        if argv[i] == "-input" and (i + 1) < len(argv): 
            input_path = argv[i + 1]
        elif argv[i] == "-texton-size" and (i + 1) < len(argv) :
            texton_size = int(argv[i + 1])
        elif argv[i] == "-output-size" and (i + 1) < len(argv) :
            output_size = int(argv[i + 1])
        elif (argv[i] == "-output" and (i + 1) < len(argv)) :
            output_path = argv[i + 1]
    input_image = read(input_path)
    image_analysis = image(input_image, texton_size, output_size, output_size)
    out_image = image_analysis.process()
    imageoutput(out_image, output_path)
