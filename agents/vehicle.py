# agents/vehicle.py


class Vehicle:
    def __init__(
        self,
        vehicle_id,
        location,
        destination,
        smart_vehicle=False,
        mode="normal",
        intersection=None,
    ):
        """
        Initialize a vehicle.

        Parameters:
            vehicle_id (str): Unique identifier for the vehicle.
            location (tuple): (latitude, longitude) of the vehicle.
            destination (str): Destination name.
            smart_vehicle (bool): True if the vehicle is equipped with smart features.
            mode (str): Current mode of the vehicle (e.g., "normal", "eco", "autonomous", "emergency").
            intersection (str): The name of the intersection the vehicle is associated with.
        """
        self.id = vehicle_id
        self.location = location
        self.destination = destination
        self.smart_vehicle = smart_vehicle
        self.mode = mode
        self.intersection = intersection

    def update_mode(self, new_mode):
        """
        Update the vehicle's operating mode.
        If the vehicle is smart, it can switch modes (eco, autonomous, emergency, etc.).
        Otherwise, it stays in normal mode.
        """
        if self.smart_vehicle:
            self.mode = new_mode
            print(f"[Vehicle] {self.id} updated mode to {self.mode}.")
        else:
            self.mode = "normal"
            print(f"[Vehicle] {self.id} is not smart, remains in normal mode.")

    def set_intersection(self, intersection):
        """
        Assign the vehicle to an intersection.
        """
        self.intersection = intersection
