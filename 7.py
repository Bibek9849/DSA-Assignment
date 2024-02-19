import tkinter as tk
from tkinter import ttk, messagebox

class GraphGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Graph GUI")

        self.graph = Graph()

        self.user_label = ttk.Label(master, text="User:")
        self.user_entry = ttk.Entry(master)
        self.user_label.grid(row=0, column=0, padx=5, pady=5)
        self.user_entry.grid(row=0, column=1, padx=5, pady=5)

        self.friend_label = ttk.Label(master, text="Friend:")
        self.friend_entry = ttk.Entry(master)
        self.friend_label.grid(row=1, column=0, padx=5, pady=5)
        self.friend_entry.grid(row=1, column=1, padx=5, pady=5)

        self.add_button = ttk.Button(master, text="Add Edge", command=self.add_edge)
        self.add_button.grid(row=2, column=0, columnspan=2, pady=10)

        self.display_button = ttk.Button(master, text="Display Graph", command=self.display_graph)
        self.display_button.grid(row=3, column=0, columnspan=2, pady=10)

        self.suggest_button = ttk.Button(master, text="Get Friend Suggestions", command=self.get_friend_suggestions)
        self.suggest_button.grid(row=4, column=0, columnspan=2, pady=10)

    def add_edge(self):
        user = self.user_entry.get()
        friend = self.friend_entry.get()

        if user and friend:
            self.graph.add_edge(user, friend)
            self.user_entry.delete(0, tk.END)
            self.friend_entry.delete(0, tk.END)

    def get_friend_suggestions(self):
        user = self.user_entry.get()
        if user in self.graph.graph_store:
            suggestions = self.graph.get_friend_suggestions(user)
            suggestion_str = f"Friend suggestions for {user}: {', '.join(suggestions)}"
            messagebox.showinfo("Friend Suggestions", suggestion_str)
        else:
            messagebox.showinfo("Friend Suggestions", f"No friend suggestions for {user}.")

    def display_graph(self):
        result = self.graph.print_graph()
        result_str = "\n".join([f"{user}: {friends}" for user, friends in result.items()])
        messagebox.showinfo("Graph Information", result_str)


class Graph:
    graph_store = dict()

    def add_edge(self, user, friend):
        if user not in self.graph_store:
            self.graph_store[user] = [friend]
        else:
            if friend not in self.graph_store[user]:
                self.graph_store[user].append(friend)

        if friend not in self.graph_store:
            self.graph_store[friend] = [user]
        else:
            if user not in self.graph_store[friend]:
                self.graph_store[friend].append(user)

    def get_friend_suggestions(self, user):
        if user in self.graph_store:
            friends_of_friends = set()
            for friend in self.graph_store[user]:
                friends_of_friends.update(self.graph_store[friend])
            # Remove user and direct friends from suggestions
            suggestions = friends_of_friends - {user} - set(self.graph_store[user])
            return list(suggestions)
        else:
            return []

    def print_graph(self):
        return self.graph_store


if __name__ == "__main__":
    root = tk.Tk()
    app = GraphGUI(root)
    root.mainloop()