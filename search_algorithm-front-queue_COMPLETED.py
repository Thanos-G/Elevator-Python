""" ----------------------------------------------------------------------------
******** Απαλλακτική Εργασία στο μάθημα της Τεχνητής Νοημοσύνης
******** Το πρόβλημα της εκκένωσης κτηρίου προς την ταράτσα
********
******** Μαρία Βοϊδονικόλα ΑΜ:19*****7
******** Γιαλαμάς Αθανάσιος ΑΜ:71*****0
********
******** Search Code for DFS, BFS and an heuristic search method
******** (expanding front and extending queue)
********
******** Κώδικας για DFS, BFS και μία ευριστική μέθοδο αναζήτησης
******** (επέκταση μετώπου και διαχείριση ουράς)
"""

import copy

import sys

sys.setrecursionlimit(10 ** 6)


# ******** Operators
# ******** Τελεστές

# Αν το ασανσέρ πάει στην ταράτσα, επιστρέφει λίστα με τη νέα κατάσταση του,
# αλλάζοντας μόνο την τελευταία θέση, που υποδεικνύει το "άδειασμα" του ασανσέρ
def go_to_roof(state):
    all_floors_empty = all(state[i] == 0 for i in range(1, 5))
    if state[-1] == 8 or all_floors_empty:
        return [5] + [state[1]] + [state[2]] + [state[3]] + [state[4]] + [0]
    else:
        return None


# Αν το ασανσέρ πάει στο 1ο όροφο, επιστρέφεται η νέα κατάσταση αφαιρώντας από τον πρώτο όροφο
# τόσα άτομα όσα η εναπομένουσα χωρητικότητα του ασανσέρ, γεμίζοντας το ασανσέρ, εκτός
# αν τα άτομα του 1ου ορόφου είναι λιγότερα, επομένως μένει άδειος και προστίθενται όλα
# τα άτομά του στο ασανσέρ.
def go_to_floor1(state):
    if state[-1] < 8 and state[1] > 0:
        if state[1] > 8 - state[-1]:
            new_state = [1] + [state[1] + state[-1] - 8] + [state[2]] + [state[3]] + [state[4]] + [8]
        else:
            new_state = [1] + [0] + [state[2]] + [state[3]] + [state[4]] + [state[1] + state[-1]]
        return new_state


# Αν το ασανσέρ πάει στο 2ο όροφο, επιστρέφεται η νέα κατάσταση αφαιρώντας από τον δεύτερο όροφο
# τόσα άτομα όσα η εναπομένουσα χωρητικότητα του ασανσέρ, γεμίζοντας το ασανσέρ, εκτός
# αν τα άτομα του 2ου ορόφου είναι λιγότερα, επομένως μένει άδειος και προστίθενται όλα
# τα άτομά του στο ασανσέρ.
def go_to_floor2(state):
    if state[-1] < 8 and state[2] > 0:
        if state[2] > 8 - state[-1]:
            new_state = [2] + [state[1]] + [state[2] + state[-1] - 8] + [state[3]] + [state[4]] + [8]
        else:
            new_state = [2] + [state[1]] + [0] + [state[3]] + [state[4]] + [state[2] + state[-1]]
        return new_state


# Αν το ασανσέρ πάει στο 3ο όροφο, επιστρέφεται η νέα κατάσταση αφαιρώντας από τον τρίτο όροφο
# τόσα άτομα όσα η εναπομένουσα χωρητικότητα του ασανσέρ, γεμίζοντας το ασανσέρ, εκτός
# αν τα άτομα του 3ου ορόφου είναι λιγότερα, επομένως μένει άδειος και προστίθενται όλα
# τα άτομά του στο ασανσέρ.
def go_to_floor3(state):
    if state[-1] < 8 and state[3] > 0:
        if state[3] > 8 - state[-1]:
            new_state = [3] + [state[1]] + [state[2]] + [state[3] + state[-1] - 8] + [state[4]] + [8]
        else:
            new_state = [3] + [state[1]] + [state[2]] + [0] + [state[4]] + [state[3] + state[-1]]
        return new_state


# Αν το ασανσέρ πάει στο 4ο όροφο, επιστρέφεται η νέα κατάσταση αφαιρώντας από τον τέταρτο όροφο
# τόσα άτομα όσα η εναπομένουσα χωρητικότητα του ασανσέρ, γεμίζοντας το ασανσέρ, εκτός
# αν τα άτομα του 4ου ορόφου είναι λιγότερα, επομένως μένει άδειος και προστίθενται όλα
# τα άτομά του στο ασανσέρ.
def go_to_floor4(state):
    if state[-1] < 8 and state[4] > 0:
        if state[4] > 8 - state[-1]:
            new_state = [4] + [state[1]] + [state[2]] + [state[3]] + [state[4] + state[-1] - 8] + [8]
        else:
            new_state = [4] + [state[1]] + [state[2]] + [state[3]] + [0] + [state[4] + state[-1]]
        return new_state


'''
Συνάρτηση εύρεσης απογόνων της τρέχουσας κατάστασης
'''


# Δημιουργία των απογόνων της εκάστοτε κατάστασης και επιστροφή της λίστα αυτών
def find_children(state):
    children = []  # αρχικοποίηση λίστας

    roof_state = copy.deepcopy(state)  # για αντιγραφή της τρέχουσας κατάστασης κάθε ορόφου
    roof_child = go_to_roof(roof_state)

    floor1_state = copy.deepcopy(state)
    floor1_child = go_to_floor1(floor1_state)

    floor2_state = copy.deepcopy(state)
    floor2_child = go_to_floor2(floor2_state)

    floor3_state = copy.deepcopy(state)
    floor3_child = go_to_floor3(floor3_state)

    floor4_state = copy.deepcopy(state)
    floor4_child = go_to_floor4(floor4_state)

    # Έλεγχος ύπαρξης των απογόνων για την προσθήκη τους με append στο τέλος της λίστας
    if roof_child is not None:
        children.append(roof_child)

    if floor4_child is not None:
        children.append(floor4_child)

    if floor3_child is not None:
        children.append(floor3_child)

    if floor2_child is not None:
        children.append(floor2_child)

    if floor1_child is not None:
        children.append(floor1_child)

    return children


""" ----------------------------------------------------------------------------
**** FRONT
**** Διαχείριση Μετώπου
"""

""" ----------------------------------------------------------------------------
** initialization of front
** Αρχικοποίηση Μετώπου
"""


def make_front(state):
    return [state]


""" ----------------------------------------------------------------------------
**** expanding front for every method
**** επέκταση μετώπου για όλες τις μεθόδους
"""


# Επεκτείνεται το υπάρχον μέτωπο ανάλογα με τη μέθοδο και επιστρέφεται σε λίστα
def expand_front(front, method):
    if method == 'DFS':  # Αναζήτηση κατά βάθος
        if front:  # Έλεγχος αν δεν είναι άδειο το μέτωπο
            print("Front:")
            print(front)
            node = front.pop(0)  # pop για αφαίρεση πρώτου (αριστερότερου) στοιχείου ώστε να αντικατασταθεί
            for child in find_children(node):  # Προφανώς, node == ο κόμβος-κατάσταση επιλέχθηκε
                front.insert(0, child)
    # αντίστοιχα με το DFS υλοποιούνται και οι άλλες δύο μέθοδοι ως εξής:
    elif method == 'BFS':  # Αναζήτηση κατά πλάτος
        if front:
            print("Front:")
            print(front)
            node = front.pop(0)
            for child in find_children(node):
                front.append(child)
    # Ευριστική μέθοδος με κριτήριο την πληρότητα του ασανσέρ.
    # Επιλέγεται κάθε φορά η περίπτωση με το πιο γεμάτο ασανσέρ.
    elif method == 'FEF':  # "Fullest Elevator First"
        if front:
            print("Front:")
            print(front)
            node = front.pop(0)
            children = find_children(node)
            children.sort(key=lambda x: x[-1])  # ταξινόμηση με βάση το τελευταίο στοιχείο (==άτομα ασανσέρ)
            for child in children:
                front.insert(0, child)  # αποθήκευση στη λίστα όπως στην DFS

    return front


""" ----------------------------------------------------------------------------
**** QUEUE
**** Διαχείριση ουράς
"""

""" ----------------------------------------------------------------------------
** initialization of queue
** Αρχικοποίηση ουράς
"""


def make_queue(state):
    return [[state]]


""" ----------------------------------------------------------------------------
**** expanding queue
**** επέκταση ουράς
"""


# Επέκταση της δοθείσας ουράς βάση της επιλεγόμενης μεθόδου
def extend_queue(queue, method):
    queue_copy = []  # Αρχικοποίηση ουράς

    if method == 'DFS':
        print("Queue:")
        print(queue)
        node = queue.pop(0)  # επιλογή του πρώτου στοιχείου τηw
        queue_copy = copy.deepcopy(queue)  # deepcopy για αντιγραφή ουράς για αποφυγή λαθών στο πρωτότυπο
        children = find_children(node[-1])  # δημιουργία των απογόνων του τελευταίου στοιχείου
        # δημιουργία διαδρομής προς τα παιδιά
        for child in children:
            path = copy.deepcopy(node)
            path.append(child)
            queue_copy.insert(0, path)  # η νέα δημιουργηθείσα διαδρομή μπαίνει στο αριστερότερο μέρος της ουράς

    # αντίστοιχα με το DFS υλοποιούνται και οι άλλες δύο μέθοδοι ως εξής:
    elif method == 'BFS':
        print("Queue:")
        print(queue)
        node = queue.pop(0)
        queue_copy = copy.deepcopy(queue)
        children = find_children(node[-1])
        for child in children:
            path = copy.deepcopy(node)
            path.append(child)
            queue_copy.append(path)

    elif method == 'FEF':  # "Fullest Elevator First"
        node = queue.pop(0)
        queue_copy = copy.deepcopy(queue)
        children = find_children(node[-1])
        children.sort(key=lambda x: x[-1])
        for child in children:
            path = copy.deepcopy(node)
            path.append(child)
            queue_copy.insert(0, path)

    return queue_copy


""" ----------------------------------------------------------------------------
**** Basic recursive function to create search tree (recursive tree expansion)
**** Βασική αναδρομική συνάρτηση για δημιουργία δέντρου αναζήτησης (αναδρομική επέκταση δέντρου)
"""


def find_solution(front, queue, closed, goal, method):
    if not front:
        print('_NO_SOLUTION_FOUND_')

    elif front[0] in closed:  # αν η πρώτη κατάσταση έχει επισκεφτεί αφαιρείται και συνεχίζει η αναζήτηση
        new_front = copy.deepcopy(front)
        new_front.pop(0)
        new_queue = copy.deepcopy(queue)
        new_queue.pop(0)
        find_solution(new_front, new_queue, closed, goal, method)

    elif front[0] == goal:  # ΕΠΙΛΥΣΗ ΠΡΟΒΛΗΜΑΤΟΣ
        print('_GOAL_FOUND_')
        print(front[0])
        print(queue[0])

    else:
        closed.append(front[0])  # θεωρεί ότι επισκέφτηκε το τρέχοντα κώδικα
        front_copy = copy.deepcopy(front)
        front_children = expand_front(front_copy, method)  # δημιουργία απογόνων - πρόσθεση τους στον τρέχον κόμβο-γονέα
        queue_copy = copy.deepcopy(queue)
        queue_children = extend_queue(queue_copy, method)  # επέκταση της ουράς
        closed_copy = copy.deepcopy(closed)  # αντιγραφή της λίστας των κόμβων που έχουν επισκεφτεί
        # αναδρομική κλήση της συνάρτησης με το ανανεωμένο μέτωπο, ουρά και τη νέα λίστα των κόμβων που έχουν επισκεφτεί
        find_solution(front_children, queue_children, closed_copy, goal, method)


"""" ----------------------------------------------------------------------------
** Executing the code
** κλήση εκτέλεσης κώδικα
"""


# Για αρχικοποίηση και επιλογή μεθόδου
def main():
    initial_state = [0, 9, 4, 12, 7, 0]
    """ ----------------------------------------------------------------------------
    **** [όροφος ασανσέρ, ένοικοι 1ου, ένοικοι 2ου, ένοικοι 3ου, ένοικοι 4ου, άτομα στο ασανσέρ]
    """
    goal = [5, 0, 0, 0, 0, 0]

    method = input('Choose searching method (DFS, BFS or FEF):\n')

    """ ----------------------------------------------------------------------------
    **** starting search
    **** έναρξη αναζήτησης
    """
    if method == 'DFS':
        print('____BEGIN__SEARCHING__FOR__DFS____')
        find_solution(make_front(initial_state), make_queue(initial_state), [], goal, method)
    elif method == 'BFS':
        print('____BEGIN__SEARCHING__FOR__BFS____')
        find_solution(make_front(initial_state), make_queue(initial_state), [], goal, method)
    elif method == 'FEF':
        print('____BEGIN__SEARCHING__FOR__FEF____')
        find_solution(make_front(initial_state), make_queue(initial_state), [], goal, method)


if __name__ == "__main__":
    main()
