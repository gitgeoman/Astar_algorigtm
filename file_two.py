
def process_func(idx, tile):
  dataset = tile['dataset']
  save_tile_img(
     tif_url,
     tile['xyz'],
     tile_size,
     save_path=img_path,
     prefix=f'znz001{dataset}_',
     display=False
  )

def main():
   ans = []
   with concurrent.futures.ProcessPoolExecutor() as executor:
      results = executor.map(process_func,tqdm(tiles_gdf.iterrows()))
   for result in results:
      ans.append(result)
   return ans

if __name__ == '__main__':
   main()