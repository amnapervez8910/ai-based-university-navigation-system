import speech_recognition as sr
import pyttsx3
import spacy
from typing import List, Tuple, Dict, Optional
import warnings
warnings.filterwarnings('ignore')

class CampusNavigationSystem:
    """
    Main class for the AI-Based University Navigation System.
    Handles speech recognition, NLP processing, pathfinding, and voice output.
    """
    
    def __init__(self):
        """Initialize the navigation system with all components."""
        # Initialize text-to-speech engine
        self.tts_engine = pyttsx3.init()
        self.setup_voice_properties()
        
        # Initialize speech recognizer
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
        # Load spaCy NLP model (small English model)
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except OSError:
            print("Downloading spaCy model...")
            import subprocess
            subprocess.run(["python", "-m", "spacy", "download", "en_core_web_sm"])
            self.nlp = spacy.load("en_core_web_sm")
        
        # Define campus locations (nodes)
        self.locations = [
            "Main gate", "Tuc Shop", "CS Department", "Computer Arts Department",
            "Hostel Area", "Tennis Court", "Admission Block", "Admission Offices",
            "Cafeteria", "Gate #5", "Sports & Gym Block", "Library", "Auditorium",
            "Administration Building", "Parking Area", "Medical Center"
        ]
        
        # Create graph representation (undirected weighted graph)
        self.graph = self.build_campus_graph()
        
        # Adjust microphone for ambient noise
        self.adjust_microphone()
        
    def setup_voice_properties(self):
        """Configure voice properties for TTS."""
        voices = self.tts_engine.getProperty('voices')
        if voices:
            self.tts_engine.setProperty('voice', voices[0].id)  # Use first available voice
        self.tts_engine.setProperty('rate', 150)  # Speed of speech
        self.tts_engine.setProperty('volume', 0.9)  # Volume level
        
    def adjust_microphone(self):
        """Adjust microphone for ambient noise."""
        try:
            with self.microphone as source:
                print("Adjusting for ambient noise... Please wait.")
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
            print("Microphone ready!")
        except Exception as e:
            print(f"Microphone adjustment warning: {e}")
    
    def build_campus_graph(self) -> Dict[str, Dict[str, int]]:
        """
        Build the campus graph representation.
        
        Returns:
            Dictionary representing graph with nodes and weighted edges
        """
        graph = {
            "Main gate": {"Tuc Shop": 5, "Tennis Court": 8, "Parking Area": 3},
            "Tuc Shop": {"Main gate": 5, "Computer Arts Department": 4, "Hostel Area": 6},
            "CS Department": {"Sports & Gym Block": 3, "Library": 4, "Cafeteria": 5},
            "Computer Arts Department": {"Tuc Shop": 4, "Hostel Area": 3, "Auditorium": 6},
            "Hostel Area": {"Computer Arts Department": 3, "Tuc Shop": 6, "Cafeteria": 7, "Medical Center": 4},
            "Tennis Court": {"Main gate": 8, "Admission Block": 3, "Sports & Gym Block": 5},
            "Admission Block": {"Tennis Court": 3, "Admission Offices": 2, "Administration Building": 4},
            "Admission Offices": {"Admission Block": 2, "Cafeteria": 4, "Administration Building": 3},
            "Cafeteria": {"Admission Offices": 4, "Hostel Area": 7, "CS Department": 5, "Gate #5": 3},
            "Gate #5": {"Cafeteria": 3, "Sports & Gym Block": 4, "Parking Area": 5},
            "Sports & Gym Block": {"Gate #5": 4, "Tennis Court": 5, "CS Department": 3, "Library": 2},
            "Library": {"CS Department": 4, "Sports & Gym Block": 2, "Auditorium": 3},
            "Auditorium": {"Library": 3, "Computer Arts Department": 6, "Administration Building": 5},
            "Administration Building": {"Auditorium": 5, "Admission Block": 4, "Admission Offices": 3},
            "Parking Area": {"Main gate": 3, "Gate #5": 5, "Medical Center": 4},
            "Medical Center": {"Parking Area": 4, "Hostel Area": 4}
        }
        return graph
    
    def speak(self, text: str):
        """
        Convert text to speech.
        
        Args:
            text: Text to be spoken
        """
        print(f"System: {text}")
        self.tts_engine.say(text)
        self.tts_engine.runAndWait()
    
    def listen_for_query(self) -> Optional[str]:
        """
        Listen for user speech input.
        
        Returns:
            Transcribed text or None if failed
        """
        try:
            with self.microphone as source:
                print("\n🎤 Listening for your query...")
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
                
            print("Processing speech...")
            text = self.recognizer.recognize_google(audio)
            print(f"You said: {text}")
            return text.lower()
            
        except sr.UnknownValueError:
            print("Sorry, I couldn't understand that.")
            self.speak("Sorry, I couldn't understand what you said. Please try again.")
            return None
        except sr.RequestError as e:
            print(f"Speech recognition service error: {e}")
            self.speak("There was an error with the speech recognition service.")
            return None
        except sr.WaitTimeoutError:
            print("No speech detected.")
            return None
    
    def extract_locations(self, query: str) -> Tuple[Optional[str], Optional[str]]:
        """
        Extract start and destination locations from query using NLP.
        
        Args:
            query: User's text query
            
        Returns:
            Tuple of (start_location, destination_location)
        """
        # Process the query with spaCy
        doc = self.nlp(query)
        
        # Extract potential location names
        found_locations = []
        
        # Check each token and entity in the query
        for token in doc:
            # Check individual tokens
            for location in self.locations:
                if location.lower() in token.text.lower():
                    if location not in found_locations:
                        found_locations.append(location)
        
        # Also check the entire query for multi-word locations
        for location in self.locations:
            if location.lower() in query:
                if location not in found_locations:
                    found_locations.append(location)
        
        # For queries with "from X to Y" structure
        start = None
        destination = None
        
        if "from" in query and "to" in query:
            parts = query.split("to")
            if len(parts) >= 2:
                from_part = parts[0].split("from")[-1].strip()
                to_part = parts[1].strip()
                
                for location in self.locations:
                    if location.lower() in from_part.lower():
                        start = location
                    if location.lower() in to_part.lower():
                        destination = location
        
        # If structure-based extraction failed, use found locations
        if not start and len(found_locations) >= 1:
            start = found_locations[0]
        if not destination and len(found_locations) >= 2:
            destination = found_locations[1]
        elif not destination and len(found_locations) == 1:
            destination = found_locations[0]
        
        return start, destination
    
    def dfs_find_paths(self, graph: Dict, start: str, destination: str, 
                       path: List = None, paths: List = None) -> List[List[str]]:
        """
        Find all possible paths using Depth-First Search.
        
        Args:
            graph: Graph representation
            start: Starting node
            destination: Destination node
            path: Current path being explored
            paths: List of all found paths
            
        Returns:
            List of all paths from start to destination
        """
        if path is None:
            path = [start]
        if paths is None:
            paths = []
        
        if start == destination:
            paths.append(path.copy())
            return paths
        
        if start not in graph:
            return paths
        
        for neighbor in graph[start]:
            if neighbor not in path:
                path.append(neighbor)
                self.dfs_find_paths(graph, neighbor, destination, path, paths)
                path.pop()
        
        return paths
    
    def format_directions(self, path: List[str]) -> str:
        """
        Format the path into readable directions.
        
        Args:
            path: List of locations in the path
            
        Returns:
            Formatted directions string
        """
        if not path:
            return "No path found."
        
        directions = f"Here's the route from {path[0]} to {path[-1]}: "
        
        for i in range(len(path) - 1):
            current = path[i]
            next_loc = path[i + 1]
            directions += f"Go from {current} to {next_loc}"
            
            # Add distance if available
            if current in self.graph and next_loc in self.graph[current]:
                distance = self.graph[current][next_loc]
                directions += f" ({distance} minutes), "
            else:
                directions += ", "
        
        directions = directions.rstrip(", ") + "."
        return directions
    
    def calculate_path_distance(self, path: List[str]) -> int:
        """
        Calculate total distance for a path.
        
        Args:
            path: List of locations
            
        Returns:
            Total distance in minutes
        """
        total = 0
        for i in range(len(path) - 1):
            current = path[i]
            next_loc = path[i + 1]
            if current in self.graph and next_loc in self.graph[current]:
                total += self.graph[current][next_loc]
        return total
    
    def provide_navigation(self, start: str, destination: str):
        """
        Provide navigation directions to the user.
        
        Args:
            start: Starting location
            destination: Destination location
        """
        if start not in self.graph:
            self.speak(f"Sorry, '{start}' is not a recognized location on campus.")
            return
        
        if destination not in self.graph:
            self.speak(f"Sorry, '{destination}' is not a recognized location on campus.")
            return
        
        # Find all possible paths using DFS
        all_paths = self.dfs_find_paths(self.graph, start, destination)
        
        if not all_paths:
            self.speak(f"Sorry, I couldn't find a path from {start} to {destination}.")
            return
        
        # Sort paths by distance (shortest first)
        all_paths.sort(key=lambda p: self.calculate_path_distance(p))
        
        # Provide the shortest path
        shortest_path = all_paths[0]
        directions = self.format_directions(shortest_path)
        distance = self.calculate_path_distance(shortest_path)
        
        self.speak(directions)
        self.speak(f"The total estimated travel time is about {distance} minutes.")
        
        # Offer alternative routes if available
        if len(all_paths) > 1:
            self.speak(f"There are {len(all_paths) - 1} alternative routes available.")
            print(f"\nAlternative paths found: {len(all_paths)} total routes")
    
    def display_available_locations(self):
        """Display all available campus locations."""
        print("\n" + "="*50)
        print("AVAILABLE CAMPUS LOCATIONS:")
        print("="*50)
        for i, location in enumerate(sorted(self.locations), 1):
            print(f"{i:2}. {location}")
        print("="*50)
    
    def run_text_mode(self):
        """Run the system in text input mode (for testing without microphone)."""
        self.speak("Welcome to the AI-Based University Navigation System!")
        self.speak("You are now in text mode. Please type your queries.")
        
        while True:
            print("\n" + "-"*50)
            query = input("You: ").strip()
            
            if query.lower() in ['exit', 'quit', 'bye']:
                self.speak("Thank you for using the campus navigation system. Goodbye!")
                break
            
            if query.lower() == 'help':
                self.display_available_locations()
                print("\nExample queries:")
                print("  - 'How do I get from Main gate to CS Department?'")
                print("  - 'Show me path from Hostel Area to Library'")
                print("  - 'Navigate from Parking Area to Cafeteria'")
                continue
            
            start, destination = self.extract_locations(query)
            
            if start and destination:
                self.provide_navigation(start, destination)
            else:
                self.display_available_locations()
                self.speak("I couldn't identify the locations in your query. Please try again.")
                print("\nExample: 'How do I get from Main gate to CS Department?'")
    
    def run_voice_mode(self):
        """Run the system in voice input mode."""
        self.speak("Welcome to the AI-Based University Navigation System!")
        self.speak("Please speak your query clearly. Say 'exit' to quit or 'help' for available locations.")
        
        while True:
            query = self.listen_for_query()
            
            if query is None:
                continue
            
            if query.lower() in ['exit', 'quit', 'bye']:
                self.speak("Thank you for using the campus navigation system. Goodbye!")
                break
            
            if 'help' in query.lower():
                self.display_available_locations()
                self.speak("You can ask for directions like: How do I get from Main gate to CS Department?")
                continue
            
            start, destination = self.extract_locations(query)
            
            if start and destination:
                self.provide_navigation(start, destination)
            else:
                self.display_available_locations()
                self.speak("I couldn't identify the locations. Please try again with a clear query.")
                self.speak("For example: How do I get from Main gate to CS Department?")


def main():
    """Main function to run the navigation system."""
    print("\n" + "="*60)
    print("   AI-BASED UNIVERSITY NAVIGATION SYSTEM")
    print("="*60)
    print("\nThis system helps you navigate around the university campus.")
    print("It uses speech recognition, NLP, and text-to-speech technology.\n")
    
    # Initialize the navigation system
    nav_system = CampusNavigationSystem()
    
    # Ask user for input mode
    print("\nSelect input mode:")
    print("1. Voice Mode (speak your queries)")
    print("2. Text Mode (type your queries - good for testing)")
    print("3. Show available locations and exit")
    
    choice = input("\nEnter your choice (1/2/3): ").strip()
    
    if choice == '1':
        nav_system.run_voice_mode()
    elif choice == '2':
        nav_system.run_text_mode()
    else:
        nav_system.display_available_locations()
        print("\nExiting system...")


if __name__ == "__main__":
    main()
