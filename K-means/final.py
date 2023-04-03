import csv
import random
import math

# Defines an x/y or lat/long coordinate.
class Coordinate:
  def __init__(self, x, y):
    self.x = x
    self.y = y

  def __str__(self):
    return "(" + str(self.x) + "," + str(self.y) + ")"
  def __repr__(self):
    return "(" + str(self.x) + "," + str(self.y) + ")"

# Defines an attraction and its lat/long x/y coordinates and its attraction type.
class Attraction:
  def __init__(self, x, y, type, hotel, name):
    self.coordinate = Coordinate(float(x), float(y))
    self.type = type
    self.hotel = hotel
    self.name = name

# Reads in an attractions csv file and converts it to a list of Attraction objects.
def read_attractions_file(filename):
  attractions = []
  with open(filename) as attractions_file:
    attractions_reader = csv.reader(attractions_file, delimiter=',')
    for row in attractions_reader:
      if row[0] == 'X-coord':
        # Skip header row
        continue
      # ['X-coord'] = 0
      # ['Y-coord'] = 1
      # ['Attraction Type'] = 2
      # ['Hotel?'] = 3
      # ['Attraction Name'] = 4
      attraction = Attraction(row[0], row[1], row[2], row[3], row[4])
      attractions.append(attraction)
  return attractions

def coordinates_distance(coord1, coord2):
  distance_sum = math.pow(coord1.x - coord2.x, 2)
  distance_sum = distance_sum + math.pow(coord1.y - coord2.y, 2)
  return math.sqrt(distance_sum)

def update_mean(mean, cluster_count, added_coordinate):
  new_mean_x = float(float(mean.x)*float(cluster_count-1)+float(added_coordinate.x))/float(cluster_count)
  new_mean_y = float(float(mean.y)*float(cluster_count-1)+float(added_coordinate.y))/float(cluster_count)
  new_mean = Coordinate(new_mean_x, new_mean_y)
  return new_mean

# Finds and returns the mean that this attraction is closest to.
def closest_mean(means, attraction):
  closest_mean_index = 0
  minimum_mean_dist = coordinates_distance(attraction.coordinate, means[closest_mean_index])

  for curr_mean_index in range(len(means)):
    distance = coordinates_distance(attraction.coordinate, means[curr_mean_index])

    if distance < minimum_mean_dist:
      minimum_mean_dist = distance
      closest_mean_index = curr_mean_index
  
  return closest_mean_index

# Performs the k-means clustering on the given list of attractions and specified "k" clusters.
def k_means_clustering(attractions, k, max_iterations=100000):

  ### 1. Initialize the algorithm.
  # Initialize the means by choosing "k" random x-y coordinates from the attractions list.
  init_mean_attractions = random.choices(attractions, k=k)
  # Take the coordinates from the k random attractions as the means.
  means = list(map(lambda a: a.coordinate, init_mean_attractions))
  # Track the size of each cluster so we can more efficiently recalculate the means as needed.
  cluster_sizes = [0 for i in range(k)]

  ### 2. Calculate the means using the following nested loop.
  # Iterate n times or until an optimal solution is reached.
  for iteration in range(max_iterations):
    # Track whether there have been any changes for this iteration. If there hasn't, then the clustering is already optimal.
    has_changed = False
    # Check each attraction and assign them to clusters based on the cluster means.
    # Then update each mean for the cluster based on its new attractions.
    for index in range(len(attractions)):
      current_attraction = attractions[index]
      # Get the index of the current closest mean to the current attraction.
      closest_mean_index = closest_mean(means, current_attraction)
      # Add this attraction to the cluster for this mean.
      cluster_sizes[closest_mean_index] += 1
      # Update the mean value since a new attraction has been added to this cluster.
      new_mean = update_mean(means[closest_mean_index], cluster_sizes[closest_mean_index], current_attraction.coordinate)
      means[closest_mean_index] = new_mean
    # if(not has_changed):
    #   # This iteration did not change any clusters. Thus, we are done.
    #   break

  ### 3. With the final means calculated, assign the attractions to their closest means, creating the clusters.
  # Initialize the clusters to empty lists for k clusters.
  clusters = [[] for i in range(k)]
  for attraction_to_add in attractions:
    closest_mean_index = closest_mean(means, attraction_to_add)
    clusters[closest_mean_index].append(attraction_to_add)
  print(means)
  return clusters

# Finds and returns the score of the cluster (The points for all attractions is initialized to 1 and can be changed by input)
def score_cluster(cluster, resturant=1, historical_site=1, bar=1, recreational_area=1, museum=1, pint_of_interest=1, activity=1, hotel=1):
  total_score = 0
  # go throught the cluster and adding the relative points to the total socre based on the attraction type
  for index in range(len(cluster)):
    attraction_type = cluster[index].type
    match attraction_type:
      case "Restaurant":
        total_score += resturant
      case "Historical site":
        total_score += historical_site
      case "Bar":
        total_score += bar
      case "Recreational area":
        total_score += recreational_area
      case "Museum":
        total_score += museum
      case "Point of interest":
        total_score += pint_of_interest
      case "Activity":
        total_score += activity
      case "Hotel":
        total_score += hotel
      case _:
        print("Invalid type:" + cluster[index].type)
  return total_score

# Finds and returns the cluster with the highest score 
def find_cluster_with_highest_score(clusters):
  cluster = 0
  cluster_with_highest_score = 0
  for index in range(len(clusters)):
    current_score = score_cluster(clusters[index])
    if (current_score>cluster_with_highest_score):
      cluster_with_highest_score = current_score
      cluster = clusters[index]
  print("The highest score is " + str(cluster_with_highest_score))
  return cluster
  
# Get Attraction objects from file.
input_attractions = read_attractions_file('./attractions.csv')
# Perform the k-means clustering. The result of this function is a list of clusters which each contains a set of attractions and hotels.
clustering_result = k_means_clustering(input_attractions, 3)

for index in range(len(clustering_result)):
  print("")
  print("Cluster " + str(index) + ": " + str(list(map(lambda x: x.coordinate, clustering_result[index]))))
  print("The total score for this cluster is " + str(score_cluster(clustering_result[index])))

print("The best cluster : " + str(list(map(lambda x: x.coordinate, find_cluster_with_highest_score(clustering_result)))))





