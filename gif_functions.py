import os
import glob
from PIL import Image
import shutil
import imageio
import datetime
import sys

def extractFrames(gifsNames):
	metadata = []
	for name in gifsNames:

			outFolder = 'frames/' + name.replace(" ","_")
			gifFile = ('source/') + name.replace(" ","_") + '.gif'

			#remove
			if os.path.exists(outFolder):
					files = glob.glob((outFolder + '/*'))
					for f in files:
							os.remove(f)
			else:
					os.makedirs(outFolder)

			frame = Image.open(gifFile)
			width, height = frame.size
			nframes = 0
			while frame:
					frame.save( '%s/frame-%s.gif' % (outFolder, nframes ) , 'GIF')
					nframes += 1
					try:
							frame.seek( nframes )
					except EOFError:
							break;

			metadata.append({'frames': nframes, 'w':width, 'h':height})

			#remove
			os.remove(gifFile)

	return metadata


def getFileNames(metadata, gifsNames):
		i = 0
		minFramesObj = min(metadata, key=lambda x:x['frames'])
		filenames = []
		while i < minFramesObj['frames']:
				for gif in gifsNames:
						name = 'frames/' + gif.replace(" ","_") + '/frame-' + str(i) + '.gif'
						filenames.append(name)
				i += 1
		return filenames

def resizeFiles(filenames, metadata, direction="horizontal"):
		minW = min(metadata, key=lambda x:x['w'])
		minH = min(metadata, key=lambda x:x['h'])
		
		for filename in filenames:
				try:
						img = Image.open(filename)
						if(direction=="horizontal"):
								h = minH['h']
								hpercent = (h/float(img.size[1]))
								w = int((float(img.size[0])*float(hpercent)))
						else:
								w = minW['w']
								wpercent = (w/float(img.size[0]))
								h = int((float(img.size[1])*float(wpercent)))
						
						img = img.resize((w,h), Image.ANTIALIAS)
						img.save(filename)
				except IOError as e: raise

		return True

def createGIF(filenames,suffix="merge"):
    images = []
    for filename in filenames:
        images.append(imageio.imread(filename))
    output_file = 'result/'+suffix+'-%s.gif' % datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    kwargs = {'fps': 20}
    imageio.mimsave(output_file, images, format='GIF', **kwargs)
    #remove
    shutil.rmtree('temp/'+suffix)
    return output_file

def createChunks(l, n):
    for i in range(0, len(l), n):
        yield l[i:i+n]

# Main functions

def gifMerge(gifsNames):

    #extract
    metadata = extractFrames(gifsNames)

    #frames
    filenames = getFileNames(metadata, gifsNames)
    
    #resize
    resizeFiles(filenames, metadata)
    
    #merge
    createGIF(filenames)


def gifConcat(gifsNames, direction="horizontal"):
    
    temptitle = "_".join(list(map(lambda n: n.replace(" ","_"), gifsNames)))

    #extract
    metadata = extractFrames(gifsNames)

    #frames
    filenames = getFileNames(metadata, gifsNames)
    
    #resize
    resizeFiles(filenames, metadata, direction)
    
    #chunks
    chunks = list(createChunks(filenames, len(gifsNames)))
    
    #concat
    frame = 0
    outFolder = 'temp/'+temptitle
    
    #remove
    if os.path.exists(outFolder):
        files = glob.glob((outFolder + '/*'))
        for f in files:
            os.remove(f)
    else:
				os.makedirs(outFolder)
    
    names = []
    for frames in chunks:
        images = list(map(Image.open, frames))
        widths, heights = zip(*(i.size for i in images))

        if(direction=="horizontal"):
            total_width = sum(widths)
            max_height = max(heights)
        
            new_im = Image.new('RGB', (total_width, max_height))

            x_offset = 0
            for im in images:
                new_im.paste(im, (x_offset,0))
                x_offset += im.size[0]

        else :
            total_height = sum(heights)
            max_width = max(widths)
        
            new_im = Image.new('RGB', (max_width, total_height))

            y_offset = 0
            for im in images:
                x_offset = int((max_width-im.size[0]) / 2)
                new_im.paste(im, (x_offset,y_offset))
                y_offset += im.size[1]

        temp_name = 'temp/'+temptitle+'/f-'+str(frame)+'.gif'
        new_im.save(temp_name)
        names.append(temp_name)
        frame += 1
    
    #remove
    for gn in gifsNames:
    		shutil.rmtree('frames/'+gn.replace(" ","_"))

    #create GIF
    return createGIF(names,temptitle)
    