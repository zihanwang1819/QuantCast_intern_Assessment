To run the project, use "python most_active_cookie.py cookie_log.csv -d 2018-12-08" as described in prject description and feel free to change query date.

most_active_cookie.py use two hashmap and a priority queue to find most active cookie(s), here is an overview of basic structure

hashmap1: save all cookies with their corresponding date, use example from description:

  key,        value
  2018-12-09, [AtY0laUfhglK3lC7, SAZuXPGUrfbcn5UA, 5UAVanZf6UtGyKVS, AtY0laUfhglK3lC7]
  2018-12-08, [SAZuXPGUrfbcn5UA, 4sMM2LxV07bPJzwf, fbcn5UAVanZf6UtG]
  2018-12-07, [4sMM2LxV07bPJzwf]
  
hashmap2: count the frequency of each cookie with in that date. use 2018-12-09 as query date as an example:
  key,              value
  AtY0laUfhglK3lC7, -2
  SAZuXPGUrfbcn5UA, -1
  5UAVanZf6UtGyKVS, -1
  
Note we use negitive value here as we use Max heap to pop largested element here, as python do not have build-in max heap, we use negitive value to simulate a max heap based on a min heap.

After poping the most active cookie, we record its frequency and poping all cookies that share the same frequency, amd save all poped elements into a list then return the list as result.

A good point of using heap is we can easyily expend the program into a find top-k most active cookie solution in future and also make it easy to find most active cookie from multiple days.




  


