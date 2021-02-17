int readRawYUV(const char *filename, uint32_t width, uint32_t height, uint8_t **YUV)
{
	FILE *fp = fopen(filename, "rb");
	if(!fp)
	{
		perror("Error opening yuv image for read");
		return 1;
	}
	
	// check file size
	fseek(fp, 0, SEEK_END);
	uint32_t size = ftell(fp);
	if(size!=(width*height + 2*((width+1)/2)*((height+1)/2)))
	{
		fprintf(stderr, "Wrong size of yuv image : %d bytes, expected %d bytes\n", size, (width*height + 2*((width+1)/2)*((height+1)/2)));
		fclose(fp);
		return 2;
	}
	fseek(fp, 0, SEEK_SET);
	
	*YUV = malloc(size);
	size_t result = fread(*YUV, 1, size, fp);
	if (result != size) {
		perror("Error reading yuv image");
		fclose(fp);
		return 3;
	}
	fclose(fp);
	return 0;
}

// write a raw yuv image file
int saveRawYUV(const char *filename, uint32_t width, uint32_t height, const uint8_t *YUV, size_t y_stride, size_t uv_stride)
{
	FILE *fp = fopen(filename, "wb");
	if(!fp)
	{
		perror("Error opening yuv image for write");
		return 1;
	}
	
	if(y_stride==width)
	{
		fwrite(YUV, 1, width*height, fp);
		YUV+=width*height;
	}
	else
	{
		for(uint32_t y=0; y<height; ++y)
		{
			fwrite(YUV, 1, width, fp);
			YUV+=y_stride;
		}
	}
	
	
	if(uv_stride==(width+1/2))
	{
		fwrite(YUV, 1, ((width+1)/2)*((height+1)/2)*2, fp);
	}
	else
	{
		for(uint32_t y=0; y<((height+1)/2); ++y)
		{
			fwrite(YUV, 1, ((width+1)/2), fp);
			YUV+=uv_stride;
		}
		
		for(uint32_t y=0; y<((height+1)/2); ++y)
		{
			fwrite(YUV, 1, ((width+1)/2), fp);
			YUV+=uv_stride;
		}
	}
	
	fclose(fp);
	return 0;
}
void convert_rgb_to_rgba(const uint8_t *RGB, uint32_t width, uint32_t height, uint8_t **RGBA)
{
	*RGBA = malloc(4*width*height);
	for(uint32_t y=0; y<height; ++y)
	{
		for(uint32_t x=0; x<width; ++x)
		{
			(*RGBA)[(y*width+x)*4] = RGB[(y*width+x)*3];
			(*RGBA)[(y*width+x)*4+1] = RGB[(y*width+x)*3+1];
			(*RGBA)[(y*width+x)*4+2] = RGB[(y*width+x)*3+2];
			(*RGBA)[(y*width+x)*4+3] = 0;
		}
	}
}