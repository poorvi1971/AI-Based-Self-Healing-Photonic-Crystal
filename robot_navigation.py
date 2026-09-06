import heapq
import matplotlib.pyplot as plt


def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def astar(start, goal, grid_size=20):
    open_list = []
    heapq.heappush(open_list, (0, start))

    came_from = {}
    cost_so_far = {start: 0}

    while open_list:

        _, current = heapq.heappop(open_list)

        if current == goal:
            break

        neighbors = [
            (current[0] + 1, current[1]),
            (current[0] - 1, current[1]),
            (current[0], current[1] + 1),
            (current[0], current[1] - 1)
        ]

        for neighbor in neighbors:

            if not (
                0 <= neighbor[0] < grid_size
                and 0 <= neighbor[1] < grid_size
            ):
                continue

            new_cost = cost_so_far[current] + 1

            if (
                neighbor not in cost_so_far
                or new_cost < cost_so_far[neighbor]
            ):

                cost_so_far[neighbor] = new_cost

                priority = (
                    new_cost
                    + heuristic(neighbor, goal)
                )

                heapq.heappush(
                    open_list,
                    (priority, neighbor)
                )

                came_from[neighbor] = current

    if goal not in came_from and goal != start:
        return []

    path = []
    current = goal

    while current != start:
        path.append(current)
        current = came_from[current]

    path.append(start)
    path.reverse()

    return path


def navigate_to_damage(
    damage_x,
    damage_y,
    start=(1, 1),
    grid_size=20
):

    # Convert image coordinates to robot grid
    goal = (
        int(damage_y / 10),
        int(damage_x / 10)
    )

    path = astar(
        start,
        goal,
        grid_size
    )

    return {
        "start": start,
        "goal": goal,
        "path": path,
        "path_length": len(path)
    }


def visualize_navigation(result, grid_size=20):

    path = result["path"]

    if not path:
        print("No path found.")
        return

    x_values = [point[1] for point in path]
    y_values = [point[0] for point in path]

    plt.figure(figsize=(7, 7))

    plt.plot(
        x_values,
        y_values,
        marker="o",
        linewidth=2
    )

    plt.scatter(
        result["start"][1],
        result["start"][0],
        s=150,
        marker="s",
        label="Robot Start"
    )

    plt.scatter(
        result["goal"][1],
        result["goal"][0],
        s=150,
        marker="X",
        label="Damage Location"
    )

    plt.xlim(-1, grid_size)
    plt.ylim(-1, grid_size)

    plt.xlabel("Grid X")
    plt.ylabel("Grid Y")
    plt.title("A* Robot Navigation to Damaged Region")

    plt.grid(True)
    plt.legend()

    plt.show()


if __name__ == "__main__":

    damage_x = 121.91
    damage_y = 59.55

    result = navigate_to_damage(
        damage_x,
        damage_y
    )

    print("===================================")
    print("ROBOT NAVIGATION")
    print("===================================")

    print(
        f"Damage coordinates: "
        f"({damage_x:.2f}, {damage_y:.2f})"
    )

    print(
        f"Robot start: "
        f"{result['start']}"
    )

    print(
        f"Robot target: "
        f"{result['goal']}"
    )

    print(
        f"Path length: "
        f"{result['path_length']}"
    )

    print("\nA* Path:")

    for step, position in enumerate(
        result["path"]
    ):
        print(
            f"Step {step}: {position}"
        )

    if result["path"]:
        print("\nRobot reached the damaged region.")
    else:
        print("\nRobot could not reach the damaged region.")

    print("===================================")

    visualize_navigation(result)