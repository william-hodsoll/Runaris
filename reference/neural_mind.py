#!/usr/bin/env python3
"""
Neural Library — The Mind (planetarium)
========================================
A book is a star. A subject is a constellation. The whole reading life
of a person, floating in the void as a slow-breathing sphere of light.

Run:
    python neural_mind.py                  # demo library
    python neural_mind.py my_books.json    # your own JSON

Generates neural_mind.html and opens it. Self-contained — no internet
or Python needed once the HTML exists.
"""

import json, sys, os, webbrowser, math, time
import random as _random
from collections import defaultdict, OrderedDict

# ─── DEMO LIBRARY ─────────────────────────────────────────────────────────────
DEMO_BOOKS = [
    {"title": "Fundamentals of Wavelets", "author": "Jaideva Goswami", "year": "", "genre": "Science", "subjects": ["signal processing", "tech"], "pages": 228},
    {"title": "Data Smart", "author": "John Foreman", "year": "", "genre": "Science", "subjects": ["data science", "tech"], "pages": 235},
    {"title": "God Created the Integers", "author": "Stephen Hawking", "year": "", "genre": "Science", "subjects": ["mathematics", "tech"], "pages": 197},
    {"title": "Superfreakonomics", "author": "Stephen Dubner", "year": "", "genre": "Science", "subjects": ["economics", "science"], "pages": 179},
    {"title": "Orientalism", "author": "Edward Said", "year": "", "genre": "Non-Fiction", "subjects": ["history", "nonfiction"], "pages": 197},
    {"title": "The Nature of Statistical Learning Theory", "author": "Vladimir Vapnik", "year": "", "genre": "Science", "subjects": ["data science", "tech"], "pages": 230},
    {"title": "Integration of the Indian States", "author": "V P Menon", "year": "", "genre": "Non-Fiction", "subjects": ["history", "nonfiction"], "pages": 217},
    {"title": "The Drunkard's Walk", "author": "Leonard Mlodinow", "year": "", "genre": "Science", "subjects": ["mathematics", "science"], "pages": 197},
    {"title": "Image Processing & Mathematical Morphology", "author": "Frank Shih", "year": "", "genre": "Science", "subjects": ["signal processing", "tech"], "pages": 241},
    {"title": "How to Think Like Sherlock Holmes", "author": "Maria Konnikova", "year": "", "genre": "Non-Fiction", "subjects": ["psychology", "nonfiction"], "pages": 240},
    {"title": "Data Scientists at Work", "author": "Sebastian Gutierrez", "year": "", "genre": "Science", "subjects": ["data science", "tech"], "pages": 230},
    {"title": "Slaughterhouse Five", "author": "Kurt Vonnegut", "year": "", "genre": "Fiction", "subjects": ["classic", "fiction"], "pages": 198},
    {"title": "Birth of a Theorem", "author": "Cedric Villani", "year": "", "genre": "Science", "subjects": ["mathematics", "science"], "pages": 234},
    {"title": "Structure & Interpretation of Computer Programs", "author": "Gerald Sussman", "year": "", "genre": "Science", "subjects": ["computer science", "tech"], "pages": 240},
    {"title": "The Age of Wrath", "author": "Abraham Eraly", "year": "", "genre": "Non-Fiction", "subjects": ["history", "nonfiction"], "pages": 238},
    {"title": "The Trial", "author": "Frank Kafka", "year": "", "genre": "Fiction", "subjects": ["classic", "fiction"], "pages": 198},
    {"title": "Statistical Decision Theory'", "author": "John Pratt", "year": "", "genre": "Science", "subjects": ["data science", "tech"], "pages": 236},
    {"title": "Data Mining Handbook", "author": "Robert Nisbet", "year": "", "genre": "Science", "subjects": ["data science", "tech"], "pages": 242},
    {"title": "The New Machiavelli", "author": "H. G. Wells", "year": "", "genre": "Fiction", "subjects": ["novel", "fiction"], "pages": 180},
    {"title": "Physics & Philosophy", "author": "Werner Heisenberg", "year": "", "genre": "Philosophy", "subjects": ["science", "philosophy"], "pages": 197},
    {"title": "Making Software", "author": "Andy Oram", "year": "", "genre": "Science", "subjects": ["computer science", "tech"], "pages": 232},
    {"title": "Analysis, Vol I", "author": "Terence Tao", "year": "", "genre": "Science", "subjects": ["mathematics", "tech"], "pages": 248},
    {"title": "Machine Learning for Hackers", "author": "Drew Conway", "year": "", "genre": "Science", "subjects": ["data science", "tech"], "pages": 233},
    {"title": "The Signal and the Noise", "author": "Nate Silver", "year": "", "genre": "Science", "subjects": ["data science", "tech"], "pages": 233},
    {"title": "Python for Data Analysis", "author": "Wes McKinney", "year": "", "genre": "Science", "subjects": ["data science", "tech"], "pages": 233},
    {"title": "Introduction to Algorithms", "author": "Thomas Cormen", "year": "", "genre": "Science", "subjects": ["computer science", "tech"], "pages": 234},
    {"title": "The Beautiful and the Damned", "author": "Siddhartha Deb", "year": "", "genre": "Non-Fiction", "subjects": ["history", "nonfiction"], "pages": 198},
    {"title": "The Outsider", "author": "Albert Camus", "year": "", "genre": "Fiction", "subjects": ["classic", "fiction"], "pages": 198},
    {"title": "Complete Sherlock Holmes, The - Vol I", "author": "Arthur Conan Doyle", "year": "", "genre": "Fiction", "subjects": ["classic", "fiction"], "pages": 176},
    {"title": "Complete Sherlock Holmes, The - Vol II", "author": "Arthur Conan Doyle", "year": "", "genre": "Fiction", "subjects": ["classic", "fiction"], "pages": 176},
    {"title": "The Wealth of Nations", "author": "Adam Smith", "year": "", "genre": "Science", "subjects": ["economics", "science"], "pages": 175},
    {"title": "The Pillars of the Earth", "author": "Ken Follett", "year": "", "genre": "Fiction", "subjects": ["novel", "fiction"], "pages": 176},
    {"title": "Mein Kampf", "author": "Adolf Hitler", "year": "", "genre": "Non-Fiction", "subjects": ["autobiography", "nonfiction"], "pages": 212},
    {"title": "The Tao of Physics", "author": "Fritjof Capra", "year": "", "genre": "Science", "subjects": ["physics", "science"], "pages": 179},
    {"title": "Surely You're Joking Mr Feynman", "author": "Richard Feynman", "year": "", "genre": "Science", "subjects": ["physics", "science"], "pages": 198},
    {"title": "A Farewell to Arms", "author": "Ernest Hemingway", "year": "", "genre": "Fiction", "subjects": ["classic", "fiction"], "pages": 179},
    {"title": "The Veteran", "author": "Frederick Forsyth", "year": "", "genre": "Fiction", "subjects": ["novel", "fiction"], "pages": 177},
    {"title": "False Impressions", "author": "Jeffery Archer", "year": "", "genre": "Fiction", "subjects": ["novel", "fiction"], "pages": 177},
    {"title": "The Last Lecture", "author": "Randy Pausch", "year": "", "genre": "Non-Fiction", "subjects": ["autobiography", "nonfiction"], "pages": 197},
    {"title": "Return of the Primitive", "author": "Ayn Rand", "year": "", "genre": "Philosophy", "subjects": ["objectivism", "philosophy"], "pages": 202},
    {"title": "Jurassic Park", "author": "Michael Crichton", "year": "", "genre": "Fiction", "subjects": ["novel", "fiction"], "pages": 174},
    {"title": "A Russian Journal", "author": "John Steinbeck", "year": "", "genre": "Non-Fiction", "subjects": ["history", "nonfiction"], "pages": 196},
    {"title": "Tales of Mystery and Imagination", "author": "Edgar Allen Poe", "year": "", "genre": "Fiction", "subjects": ["classic", "fiction"], "pages": 172},
    {"title": "Freakonomics", "author": "Stephen Dubner", "year": "", "genre": "Science", "subjects": ["economics", "science"], "pages": 197},
    {"title": "The Hidden Connections", "author": "Fritjof Capra", "year": "", "genre": "Science", "subjects": ["physics", "science"], "pages": 197},
    {"title": "The Story of Philosophy", "author": "Will Durant", "year": "", "genre": "Philosophy", "subjects": ["history", "philosophy"], "pages": 170},
    {"title": "Asami Asami", "author": "P L Deshpande", "year": "", "genre": "Fiction", "subjects": ["novel", "fiction"], "pages": 205},
    {"title": "Journal of a Novel", "author": "John Steinbeck", "year": "", "genre": "Fiction", "subjects": ["classic", "fiction"], "pages": 196},
    {"title": "Once There Was a War", "author": "John Steinbeck", "year": "", "genre": "Non-Fiction", "subjects": ["history", "nonfiction"], "pages": 196},
    {"title": "The Moon is Down", "author": "John Steinbeck", "year": "", "genre": "Fiction", "subjects": ["classic", "fiction"], "pages": 196},
    {"title": "The Brethren", "author": "John Grisham", "year": "", "genre": "Fiction", "subjects": ["novel", "fiction"], "pages": 174},
    {"title": "In a Free State", "author": "V. S. Naipaul", "year": "", "genre": "Fiction", "subjects": ["novel", "fiction"], "pages": 196},
    {"title": "Catch 22", "author": "Joseph Heller", "year": "", "genre": "Fiction", "subjects": ["classic", "fiction"], "pages": 178},
    {"title": "The Complete Mastermind", "author": "BBC", "year": "", "genre": "Non-Fiction", "subjects": ["trivia", "nonfiction"], "pages": 178},
    {"title": "Dylan on Dylan", "author": "Bob Dylan", "year": "", "genre": "Non-Fiction", "subjects": ["autobiography", "nonfiction"], "pages": 197},
    {"title": "Soft Computing & Intelligent Systems", "author": "Madan Gupta", "year": "", "genre": "Science", "subjects": ["data science", "tech"], "pages": 242},
    {"title": "Textbook of Economic Theory", "author": "Alfred Stonier", "year": "", "genre": "Science", "subjects": ["economics", "tech"], "pages": 242},
    {"title": "Econometric Analysis", "author": "W. H. Greene", "year": "", "genre": "Science", "subjects": ["economics", "tech"], "pages": 242},
    {"title": "Learning OpenCV", "author": "Gary Bradsky", "year": "", "genre": "Science", "subjects": ["signal processing", "tech"], "pages": 232},
    {"title": "Data Structures Using C & C++", "author": "Andrew Tanenbaum", "year": "", "genre": "Science", "subjects": ["computer science", "tech"], "pages": 235},
    {"title": "Computer Vision, A Modern Approach", "author": "David Forsyth", "year": "", "genre": "Science", "subjects": ["signal processing", "tech"], "pages": 255},
    {"title": "Principles of Communication Systems", "author": "Schilling Taub", "year": "", "genre": "Science", "subjects": ["signal processing", "tech"], "pages": 240},
    {"title": "Let Us C", "author": "Yashwant Kanetkar", "year": "", "genre": "Science", "subjects": ["computer science", "tech"], "pages": 213},
    {"title": "The Amulet of Samarkand", "author": "Jonathan Stroud", "year": "", "genre": "Fiction", "subjects": ["novel", "fiction"], "pages": 179},
    {"title": "Crime and Punishment", "author": "Fyodor Dostoevsky", "year": "", "genre": "Fiction", "subjects": ["classic", "fiction"], "pages": 180},
    {"title": "Angels & Demons", "author": "Dan Brown", "year": "", "genre": "Fiction", "subjects": ["novel", "fiction"], "pages": 178},
    {"title": "The Argumentative Indian", "author": "Amartya Sen", "year": "", "genre": "Non-Fiction", "subjects": ["history", "nonfiction"], "pages": 209},
    {"title": "Sea of Poppies", "author": "Amitav Ghosh", "year": "", "genre": "Fiction", "subjects": ["novel", "fiction"], "pages": 197},
    {"title": "The Idea of Justice", "author": "Amartya Sen", "year": "", "genre": "Philosophy", "subjects": ["economics", "philosophy"], "pages": 212},
    {"title": "A Raisin in the Sun", "author": "Lorraine Hansberry", "year": "", "genre": "Fiction", "subjects": ["novel", "fiction"], "pages": 175},
    {"title": "All the President's Men", "author": "Bob Woodward", "year": "", "genre": "Non-Fiction", "subjects": ["history", "nonfiction"], "pages": 177},
    {"title": "A Prisoner of Birth", "author": "Jeffery Archer", "year": "", "genre": "Fiction", "subjects": ["novel", "fiction"], "pages": 176},
    {"title": "Scoop!", "author": "Kuldip Nayar", "year": "", "genre": "Non-Fiction", "subjects": ["history", "nonfiction"], "pages": 216},
    {"title": "Ahe Manohar Tari", "author": "Sunita Deshpande", "year": "", "genre": "Non-Fiction", "subjects": ["autobiography", "nonfiction"], "pages": 213},
    {"title": "The Last Mughal", "author": "William Dalrymple", "year": "", "genre": "Non-Fiction", "subjects": ["history", "nonfiction"], "pages": 199},
    {"title": "Social Choice & Welfare, Vol 39 No. 1", "author": "Various", "year": "", "genre": "Science", "subjects": ["economics", "tech"], "pages": 235},
    {"title": "Radiowaril Bhashane & Shrutika", "author": "P L Deshpande", "year": "", "genre": "Non-Fiction", "subjects": ["misc", "nonfiction"], "pages": 213},
    {"title": "Gun Gayin Awadi", "author": "P L Deshpande", "year": "", "genre": "Non-Fiction", "subjects": ["misc", "nonfiction"], "pages": 212},
    {"title": "Aghal Paghal", "author": "P L Deshpande", "year": "", "genre": "Non-Fiction", "subjects": ["misc", "nonfiction"], "pages": 212},
    {"title": "Maqta-e-Ghalib", "author": "Sanjay Garg", "year": "", "genre": "Non-Fiction", "subjects": ["poetry", "nonfiction"], "pages": 221},
    {"title": "Beyond Degrees", "author": "Unknown", "year": "", "genre": "Philosophy", "subjects": ["education", "philosophy"], "pages": 222},
    {"title": "Manasa", "author": "V P Kale", "year": "", "genre": "Non-Fiction", "subjects": ["misc", "nonfiction"], "pages": 213},
    {"title": "India from Midnight to Milennium", "author": "Shashi Tharoor", "year": "", "genre": "Non-Fiction", "subjects": ["history", "nonfiction"], "pages": 198},
    {"title": "The World's Greatest Trials", "author": "Unknown", "year": "", "genre": "Non-Fiction", "subjects": ["history", "nonfiction"], "pages": 210},
    {"title": "The Great Indian Novel", "author": "Shashi Tharoor", "year": "", "genre": "Fiction", "subjects": ["novel", "fiction"], "pages": 198},
    {"title": "O Jerusalem!", "author": "Dominique Lapierre", "year": "", "genre": "Non-Fiction", "subjects": ["history", "nonfiction"], "pages": 217},
    {"title": "The City of Joy", "author": "Dominique Lapierre", "year": "", "genre": "Fiction", "subjects": ["novel", "fiction"], "pages": 177},
    {"title": "Freedom at Midnight", "author": "Dominique Lapierre", "year": "", "genre": "Non-Fiction", "subjects": ["history", "nonfiction"], "pages": 167},
    {"title": "The Winter of Our Discontent", "author": "John Steinbeck", "year": "", "genre": "Fiction", "subjects": ["classic", "fiction"], "pages": 196},
    {"title": "On Education", "author": "Bertrand Russell", "year": "", "genre": "Philosophy", "subjects": ["education", "philosophy"], "pages": 203},
    {"title": "Free Will", "author": "Sam Harris", "year": "", "genre": "Non-Fiction", "subjects": ["psychology", "nonfiction"], "pages": 203},
    {"title": "Bookless in Baghdad", "author": "Shashi Tharoor", "year": "", "genre": "Non-Fiction", "subjects": ["history", "nonfiction"], "pages": 206},
    {"title": "The Case of the Lame Canary", "author": "Earle Stanley Gardner", "year": "", "genre": "Fiction", "subjects": ["novel", "fiction"], "pages": 179},
    {"title": "The Theory of Everything", "author": "Stephen Hawking", "year": "", "genre": "Science", "subjects": ["physics", "science"], "pages": 217},
    {"title": "New Markets & Other Essays", "author": "Peter Drucker", "year": "", "genre": "Science", "subjects": ["economics", "science"], "pages": 176},
    {"title": "Electric Universe", "author": "David Bodanis", "year": "", "genre": "Science", "subjects": ["physics", "science"], "pages": 201},
    {"title": "The Hunchback of Notre Dame", "author": "Victor Hugo", "year": "", "genre": "Fiction", "subjects": ["classic", "fiction"], "pages": 175},
    {"title": "Burning Bright", "author": "John Steinbeck", "year": "", "genre": "Fiction", "subjects": ["classic", "fiction"], "pages": 175},
    {"title": "The Age of Discontuinity", "author": "Peter Drucker", "year": "", "genre": "Non-Fiction", "subjects": ["economics", "nonfiction"], "pages": 178},
    {"title": "Doctor in the Nude", "author": "Richard Gordon", "year": "", "genre": "Fiction", "subjects": ["novel", "fiction"], "pages": 179},
    {"title": "Down and Out in Paris & London", "author": "George Orwell", "year": "", "genre": "Non-Fiction", "subjects": ["autobiography", "nonfiction"], "pages": 179},
    {"title": "Identity & Violence", "author": "Amartya Sen", "year": "", "genre": "Philosophy", "subjects": ["philosophy"], "pages": 219},
    {"title": "Beyond the Three Seas", "author": "William Dalrymple", "year": "", "genre": "Non-Fiction", "subjects": ["history", "nonfiction"], "pages": 197},
    {"title": "The World's Greatest Short Stories", "author": "Unknown", "year": "", "genre": "Fiction", "subjects": ["classic", "fiction"], "pages": 217},
    {"title": "Talking Straight", "author": "Lee Iacoca", "year": "", "genre": "Non-Fiction", "subjects": ["autobiography", "nonfiction"], "pages": 175},
    {"title": "Maugham's Collected Short Stories, Vol 3", "author": "William S Maugham", "year": "", "genre": "Fiction", "subjects": ["classic", "fiction"], "pages": 171},
    {"title": "The Phantom of Manhattan", "author": "Frederick Forsyth", "year": "", "genre": "Fiction", "subjects": ["classic", "fiction"], "pages": 180},
    {"title": "Ashenden of The British Agent", "author": "William S Maugham", "year": "", "genre": "Fiction", "subjects": ["classic", "fiction"], "pages": 160},
    {"title": "Zen & The Art of Motorcycle Maintenance", "author": "Robert Pirsig", "year": "", "genre": "Philosophy", "subjects": ["autobiography", "philosophy"], "pages": 172},
    {"title": "The Great War for Civilization", "author": "Robert Fisk", "year": "", "genre": "Non-Fiction", "subjects": ["history", "nonfiction"], "pages": 197},
    {"title": "We the Living", "author": "Ayn Rand", "year": "", "genre": "Fiction", "subjects": ["novel", "fiction"], "pages": 178},
    {"title": "The Artist and the Mathematician", "author": "Amir Aczel", "year": "", "genre": "Science", "subjects": ["mathematics", "science"], "pages": 186},
    {"title": "History of Western Philosophy", "author": "Bertrand Russell", "year": "", "genre": "Philosophy", "subjects": ["philosophy"], "pages": 213},
    {"title": "Selected Short Stories", "author": "Unknown", "year": "", "genre": "Fiction", "subjects": ["classic", "fiction"], "pages": 215},
    {"title": "Rationality & Freedom", "author": "Amartya Sen", "year": "", "genre": "Science", "subjects": ["economics", "science"], "pages": 213},
    {"title": "Clash of Civilizations and Remaking of the World Order", "author": "Samuel Huntington", "year": "", "genre": "Non-Fiction", "subjects": ["history", "nonfiction"], "pages": 228},
    {"title": "Uncommon Wisdom", "author": "Fritjof Capra", "year": "", "genre": "Non-Fiction", "subjects": ["anthology", "nonfiction"], "pages": 197},
    {"title": "One", "author": "Richard Bach", "year": "", "genre": "Non-Fiction", "subjects": ["autobiography", "nonfiction"], "pages": 172},
    {"title": "Karl Marx Biography", "author": "Unknown", "year": "", "genre": "Non-Fiction", "subjects": ["autobiography", "nonfiction"], "pages": 162},
    {"title": "To Sir With Love", "author": "Braithwaite", "year": "", "genre": "Fiction", "subjects": ["classic", "fiction"], "pages": 197},
    {"title": "Half A Life", "author": "V S Naipaul", "year": "", "genre": "Fiction", "subjects": ["novel", "fiction"], "pages": 196},
    {"title": "The Discovery of India", "author": "Jawaharlal Nehru", "year": "", "genre": "Non-Fiction", "subjects": ["history", "nonfiction"], "pages": 230},
    {"title": "Apulki", "author": "P L Deshpande", "year": "", "genre": "Non-Fiction", "subjects": ["misc", "nonfiction"], "pages": 211},
    {"title": "Unpopular Essays", "author": "Bertrand Russell", "year": "", "genre": "Philosophy", "subjects": ["philosophy"], "pages": 198},
    {"title": "The Deceiver", "author": "Frederick Forsyth", "year": "", "genre": "Fiction", "subjects": ["novel", "fiction"], "pages": 178},
    {"title": "Veil: Secret Wars of the CIA", "author": "Bob Woodward", "year": "", "genre": "Non-Fiction", "subjects": ["history", "nonfiction"], "pages": 171},
    {"title": "Char Shabda", "author": "P L Deshpande", "year": "", "genre": "Non-Fiction", "subjects": ["misc", "nonfiction"], "pages": 214},
    {"title": "Rosy is My Relative", "author": "Gerald Durrell", "year": "", "genre": "Fiction", "subjects": ["novel", "fiction"], "pages": 176},
    {"title": "The Moon and Sixpence", "author": "William S Maugham", "year": "", "genre": "Fiction", "subjects": ["classic", "fiction"], "pages": 180},
    {"title": "Political Philosophers", "author": "Unknown", "year": "", "genre": "Philosophy", "subjects": ["politics", "philosophy"], "pages": 162},
    {"title": "A Short History of the World", "author": "H G Wells", "year": "", "genre": "Non-Fiction", "subjects": ["history", "nonfiction"], "pages": 197},
    {"title": "The Trembling of a Leaf", "author": "William S Maugham", "year": "", "genre": "Fiction", "subjects": ["novel", "fiction"], "pages": 205},
    {"title": "Doctor on the Brain", "author": "Richard Gordon", "year": "", "genre": "Fiction", "subjects": ["novel", "fiction"], "pages": 204},
    {"title": "Simpsons & Their Mathematical Secrets", "author": "Simon Singh", "year": "", "genre": "Science", "subjects": ["mathematics", "science"], "pages": 233},
    {"title": "Pattern Classification", "author": "Hart Duda", "year": "", "genre": "Science", "subjects": ["data science", "tech"], "pages": 241},
    {"title": "From Beirut to Jerusalem", "author": "Thomas Friedman", "year": "", "genre": "Non-Fiction", "subjects": ["history", "nonfiction"], "pages": 202},
    {"title": "The Code Book", "author": "Simon Singh", "year": "", "genre": "Science", "subjects": ["mathematics", "science"], "pages": 197},
    {"title": "The Age of the Warrior", "author": "Robert Fisk", "year": "", "genre": "Non-Fiction", "subjects": ["history", "nonfiction"], "pages": 197},
    {"title": "Final Crisis", "author": "Unknown", "year": "", "genre": "Fiction", "subjects": ["comic", "fiction"], "pages": 257},
    {"title": "The Killing Joke", "author": "Unknown", "year": "", "genre": "Fiction", "subjects": ["comic", "fiction"], "pages": 283},
    {"title": "Flashpoint", "author": "Unknown", "year": "", "genre": "Fiction", "subjects": ["comic", "fiction"], "pages": 265},
    {"title": "Batman Earth One", "author": "Unknown", "year": "", "genre": "Fiction", "subjects": ["comic", "fiction"], "pages": 265},
    {"title": "Crisis on Infinite Earths", "author": "Unknown", "year": "", "genre": "Fiction", "subjects": ["comic", "fiction"], "pages": 258},
    {"title": "The Numbers Behind Numb3rs", "author": "Keith Devlin", "year": "", "genre": "Science", "subjects": ["mathematics", "science"], "pages": 202},
    {"title": "Superman Earth One - 1", "author": "Unknown", "year": "", "genre": "Fiction", "subjects": ["comic", "fiction"], "pages": 259},
    {"title": "Superman Earth One - 2", "author": "Unknown", "year": "", "genre": "Fiction", "subjects": ["comic", "fiction"], "pages": 258},
    {"title": "Justice League: Throne of Atlantis", "author": "Unknown", "year": "", "genre": "Fiction", "subjects": ["comic", "fiction"], "pages": 258},
    {"title": "Justice League: The Villain's Journey", "author": "Unknown", "year": "", "genre": "Fiction", "subjects": ["comic", "fiction"], "pages": 258},
    {"title": "The Death of Superman", "author": "Unknown", "year": "", "genre": "Fiction", "subjects": ["comic", "fiction"], "pages": 258},
    {"title": "History of the DC Universe", "author": "Unknown", "year": "", "genre": "Fiction", "subjects": ["comic", "fiction"], "pages": 258},
    {"title": "Batman: The Long Halloween", "author": "Unknown", "year": "", "genre": "Fiction", "subjects": ["comic", "fiction"], "pages": 258},
    {"title": "A Life in Letters", "author": "John Steinbeck", "year": "", "genre": "Non-Fiction", "subjects": ["autobiography", "nonfiction"], "pages": 196},
    {"title": "The Information", "author": "James Gleick", "year": "", "genre": "Science", "subjects": ["mathematics", "science"], "pages": 233},
    {"title": "Journal of Economics, vol 106 No 3", "author": "Unknown", "year": "", "genre": "Science", "subjects": ["economics", "science"], "pages": 235},
    {"title": "Elements of Information Theory", "author": "Joy Thomas", "year": "", "genre": "Science", "subjects": ["signal processing", "tech"], "pages": 229},
    {"title": "Power Electronics - Rashid", "author": "Muhammad Rashid", "year": "", "genre": "Science", "subjects": ["computer science", "tech"], "pages": 235},
    {"title": "Power Electronics - Mohan", "author": "Ned Mohan", "year": "", "genre": "Science", "subjects": ["computer science", "tech"], "pages": 237},
    {"title": "Neural Networks", "author": "Simon Haykin", "year": "", "genre": "Science", "subjects": ["data science", "tech"], "pages": 240},
    {"title": "The Grapes of Wrath", "author": "John Steinbeck", "year": "", "genre": "Fiction", "subjects": ["classic", "fiction"], "pages": 196},
    {"title": "Vyakti ani Valli", "author": "P L Deshpande", "year": "", "genre": "Non-Fiction", "subjects": ["misc", "nonfiction"], "pages": 211},
    {"title": "Statistical Learning Theory", "author": "Vladimir Vapnik", "year": "", "genre": "Science", "subjects": ["data science", "tech"], "pages": 228},
    {"title": "Empire of the Mughal - The Tainted Throne", "author": "Alex Rutherford", "year": "", "genre": "Non-Fiction", "subjects": ["history", "nonfiction"], "pages": 180},
    {"title": "Empire of the Mughal - Brothers at War", "author": "Alex Rutherford", "year": "", "genre": "Non-Fiction", "subjects": ["history", "nonfiction"], "pages": 180},
    {"title": "Empire of the Mughal - Ruler of the World", "author": "Alex Rutherford", "year": "", "genre": "Non-Fiction", "subjects": ["history", "nonfiction"], "pages": 180},
    {"title": "Empire of the Mughal - The Serpent's Tooth", "author": "Alex Rutherford", "year": "", "genre": "Non-Fiction", "subjects": ["history", "nonfiction"], "pages": 180},
    {"title": "Empire of the Mughal - Raiders from the North", "author": "Alex Rutherford", "year": "", "genre": "Non-Fiction", "subjects": ["history", "nonfiction"], "pages": 180},
    {"title": "Mossad", "author": "Michael Baz-Zohar", "year": "", "genre": "Non-Fiction", "subjects": ["history", "nonfiction"], "pages": 236},
    {"title": "Jim Corbett Omnibus", "author": "Jim Corbett", "year": "", "genre": "Non-Fiction", "subjects": ["history", "nonfiction"], "pages": 223},
    {"title": "20000 Leagues Under the Sea", "author": "Jules Verne", "year": "", "genre": "Fiction", "subjects": ["novel", "fiction"], "pages": 190},
    {"title": "Batatyachi Chal", "author": "Deshpande P L", "year": "", "genre": "Fiction", "subjects": ["novel", "fiction"], "pages": 200},
    {"title": "Hafasavnuk", "author": "Deshpande P L", "year": "", "genre": "Fiction", "subjects": ["novel", "fiction"], "pages": 211},
    {"title": "Urlasurla", "author": "Deshpande P L", "year": "", "genre": "Fiction", "subjects": ["novel", "fiction"], "pages": 211},
    {"title": "Pointers in C", "author": "Yashwant Kanetkar", "year": "", "genre": "Science", "subjects": ["computer science", "tech"], "pages": 213},
    {"title": "The Cathedral and the Bazaar", "author": "Eric Raymond", "year": "", "genre": "Science", "subjects": ["computer science", "tech"], "pages": 217},
    {"title": "Design with OpAmps", "author": "Sergio Franco", "year": "", "genre": "Science", "subjects": ["computer science", "tech"], "pages": 240},
    {"title": "Think Complexity", "author": "Allen Downey", "year": "", "genre": "Science", "subjects": ["data science", "tech"], "pages": 230},
    {"title": "The Devil's Advocate", "author": "Morris West", "year": "", "genre": "Fiction", "subjects": ["novel", "fiction"], "pages": 178},
    {"title": "Ayn Rand Answers", "author": "Ayn Rand", "year": "", "genre": "Philosophy", "subjects": ["objectivism", "philosophy"], "pages": 203},
    {"title": "Philosophy: Who Needs It", "author": "Ayn Rand", "year": "", "genre": "Philosophy", "subjects": ["objectivism", "philosophy"], "pages": 171},
    {"title": "The World's Great Thinkers", "author": "Unknown", "year": "", "genre": "Science", "subjects": ["physics", "science"], "pages": 189},
    {"title": "Data Analysis with Open Source Tools", "author": "Phillip Janert", "year": "", "genre": "Science", "subjects": ["data science", "tech"], "pages": 230},
    {"title": "Broca's Brain", "author": "Carl Sagan", "year": "", "genre": "Science", "subjects": ["physics", "science"], "pages": 174},
    {"title": "Men of Mathematics", "author": "E T Bell", "year": "", "genre": "Science", "subjects": ["mathematics", "science"], "pages": 217},
    {"title": "Oxford book of Modern Science Writing", "author": "Richard Dawkins", "year": "", "genre": "Science", "subjects": ["science"], "pages": 240},
    {"title": "Justice, Judiciary and Democracy", "author": "Sudhanshu Ranjan", "year": "", "genre": "Non-Fiction", "subjects": ["legal", "nonfiction"], "pages": 224},
    {"title": "The Arthashastra", "author": "Kautiyla", "year": "", "genre": "Philosophy", "subjects": ["philosophy"], "pages": 214},
    {"title": "We the People", "author": "Palkhivala", "year": "", "genre": "Philosophy", "subjects": ["philosophy"], "pages": 216},
    {"title": "We the Nation", "author": "Palkhivala", "year": "", "genre": "Philosophy", "subjects": ["philosophy"], "pages": 216},
    {"title": "The Courtroom Genius", "author": "Sorabjee", "year": "", "genre": "Non-Fiction", "subjects": ["autobiography", "nonfiction"], "pages": 217},
    {"title": "Dongri to Dubai", "author": "Hussain Zaidi", "year": "", "genre": "Non-Fiction", "subjects": ["history", "nonfiction"], "pages": 216},
    {"title": "History of England, Foundation", "author": "Peter Ackroyd", "year": "", "genre": "Non-Fiction", "subjects": ["history", "nonfiction"], "pages": 197},
    {"title": "City of Djinns", "author": "William Dalrymple", "year": "", "genre": "Non-Fiction", "subjects": ["history", "nonfiction"], "pages": 198},
    {"title": "India's Legal System", "author": "Nariman", "year": "", "genre": "Non-Fiction", "subjects": ["legal", "nonfiction"], "pages": 177},
    {"title": "More Tears to Cry", "author": "Jean Sassoon", "year": "", "genre": "Fiction", "subjects": ["novel", "fiction"], "pages": 235},
    {"title": "The Ropemaker", "author": "Peter Dickinson", "year": "", "genre": "Fiction", "subjects": ["novel", "fiction"], "pages": 196},
    {"title": "Angels & Demons", "author": "Dan Brown", "year": "", "genre": "Fiction", "subjects": ["novel", "fiction"], "pages": 170},
    {"title": "The Judge", "author": "Unknown", "year": "", "genre": "Fiction", "subjects": ["novel", "fiction"], "pages": 170},
    {"title": "The Attorney", "author": "Unknown", "year": "", "genre": "Fiction", "subjects": ["novel", "fiction"], "pages": 170},
    {"title": "The Prince", "author": "Machiavelli", "year": "", "genre": "Fiction", "subjects": ["classic", "fiction"], "pages": 173},
    {"title": "Eyeless in Gaza", "author": "Aldous Huxley", "year": "", "genre": "Fiction", "subjects": ["novel", "fiction"], "pages": 180},
    {"title": "Tales of Beedle the Bard", "author": "J K Rowling", "year": "", "genre": "Fiction", "subjects": ["novel", "fiction"], "pages": 184},
    {"title": "Girl with the Dragon Tattoo", "author": "Steig Larsson", "year": "", "genre": "Fiction", "subjects": ["novel", "fiction"], "pages": 179},
    {"title": "Girl who kicked the Hornet's Nest", "author": "Steig Larsson", "year": "", "genre": "Fiction", "subjects": ["novel", "fiction"], "pages": 179},
    {"title": "Girl who played with Fire", "author": "Steig Larsson", "year": "", "genre": "Fiction", "subjects": ["novel", "fiction"], "pages": 179},
    {"title": "Batman Handbook", "author": "Unknown", "year": "", "genre": "Fiction", "subjects": ["comic", "fiction"], "pages": 270},
    {"title": "Murphy's Law", "author": "Unknown", "year": "", "genre": "Philosophy", "subjects": ["psychology", "philosophy"], "pages": 178},
    {"title": "Structure and Randomness", "author": "Terence Tao", "year": "", "genre": "Science", "subjects": ["mathematics", "science"], "pages": 252},
    {"title": "Image Processing with MATLAB", "author": "Steve Eddins", "year": "", "genre": "Science", "subjects": ["signal processing", "tech"], "pages": 241},
    {"title": "Animal Farm", "author": "George Orwell", "year": "", "genre": "Fiction", "subjects": ["classic", "fiction"], "pages": 180},
    {"title": "The Idiot", "author": "Fyodor Dostoevsky", "year": "", "genre": "Fiction", "subjects": ["classic", "fiction"], "pages": 197},
    {"title": "A Christmas Carol", "author": "Charles Dickens", "year": "", "genre": "Fiction", "subjects": ["classic", "fiction"], "pages": 196},
]

# Subject colors — soft, luminous, planetarium hues. Picked to read as
# distinct star fields against pure black. Anything not listed gets DEFAULT.
SUBJECT_COLORS_DEFAULT = {
    # Original luminous palette
    "consciousness":   "#9bb5ff",   # cool blue-white
    "AI":              "#7fe1d4",   # turquoise
    "dystopia":        "#ff8a78",   # ember
    "mythology":       "#e8c97f",   # gold
    "religion":        "#d4a5ff",   # violet
    "identity":        "#a8e8a3",   # pale green
    "existentialism":  "#c8a4f0",   # lilac
    "power":           "#ff9ab8",   # rose
    "time":            "#9eddff",   # ice blue
    "death":           "#b4b0b0",   # bone
    "morality":        "#ffd089",   # warm amber
    "history":         "#d8b377",   # bronze
    "politics":        "#ffa07a",   # coral
    "ecology":         "#8ed68e",   # forest
    "cyberpunk":       "#c895ff",   # ultraviolet
    "memory":          "#f8c8a5",   # soft peach
    "love":            "#ff9bb0",   # warm rose
    "cosmology":       "#a0c0ff",   # deep blue
    "psychology":      "#b8a8ff",   # periwinkle
    "evolution":       "#8edca7",   # emerald
    "dreams":          "#d4a8f8",   # dream lilac
    "science":         "#7ad4e0",   # cyan
    # CSV-derived subjects
    "novel":             "#9bc8ff",   # storyteller blue
    "classic":           "#e8d4a0",   # vellum
    "data science":      "#7fe1c0",   # bright teal
    "comic":             "#ffb45e",   # vivid orange
    "mathematics":       "#a4d6ff",   # chalk blue
    "economics":         "#c8e08a",   # ledger green
    "autobiography":     "#f4a8c0",   # personal pink
    "computer science":  "#80d4ff",   # circuit cyan
    "signal processing": "#a8c4ff",   # frequency blue
    "physics":           "#94c8ff",   # quantum blue
    "objectivism":       "#ff9168",   # forge orange
    "poetry":            "#dba8e0",   # lavender
    "legal":             "#c4b094",   # parchment
    "education":         "#a0e0c4",   # mint
    "anthology":         "#e0c8e8",   # mauve
    "trivia":            "#ffd8a0",   # warm cream
    "misc":              "#b0b8c4",   # neutral grey-blue
    "philosophy":        "#c8a4f0",   # lilac (mirrors existentialism's family)
}
DEFAULT_SUBJECT_COLOR = "#7A8078"
# Earth palette — the live colour source. Cycled per constellation so
# neighbouring clusters always differ. Mid/dark tones that read on cream.
EARTH_COLORS = ["#5A7340", "#9A6C60", "#6F838C", "#D4A93E", "#414B38", "#8E7F78",
                "#5F6C78", "#B99D84", "#5A3A2C", "#7A8078", "#4D6142", "#898270"]


def build_mind(books, seed=None):
    """
    Build a constellation sphere:
      * each unique PRIMARY subject -> a "constellation centre" on a sphere shell
      * each book in that subject -> a star drifting loosely around its centre
      * connections (invisible at rest) between any pair of books sharing
        a subject, genre, or author -- a separate pool used for pulse signals
    """
    rng = _random.Random(seed if seed is not None else _random.randrange(1 << 30))

    # Group books by primary subject (their first subject tag).
    by_subject = OrderedDict()
    for b in books:
        subs = b.get("subjects", [])
        primary = subs[0] if subs else "general"
        by_subject.setdefault(primary, []).append(b)

    subjects = list(by_subject.keys())
    n_subj = len(subjects)
    if n_subj == 0:
        return {"stars": [], "centres": [], "edges": [], "subjects": []}

    # Distribute subject centres throughout the sphere VOLUME.
    # Direction comes from a Fibonacci lattice for even angular spread.
    # Radius comes from a SHUFFLED stratified set so subject order in the
    # input doesn't correlate with position — preventing "all big clusters
    # on one side" artifacts.
    SPHERE_R = 380              # outer radius of the planetarium sphere
    DRIFT    = 60               # how far stars can wander from their centre
    golden = math.pi * (1 + math.sqrt(5))

    # Build a shuffled radial sequence: stratified 0..1, then shuffled, so the
    # mapping from input order to radius is random but coverage stays uniform.
    radial_bins = [(i + 0.5) / n_subj for i in range(n_subj)]
    rng.shuffle(radial_bins)
    # Same idea for an angular shuffle: instead of theta = golden * i, we
    # randomise which lattice slot each subject takes.
    lattice_slots = list(range(n_subj))
    rng.shuffle(lattice_slots)

    centres = []
    for i, subj in enumerate(subjects):
        slot = lattice_slots[i]
        t_lat = (slot + 0.5) / n_subj
        phi   = math.acos(1 - 2 * t_lat)
        theta = golden * slot
        # small jitter so the lattice doesn't look mechanical
        phi   += rng.uniform(-0.06, 0.06)
        theta += rng.uniform(-0.06, 0.06)

        # Radial position from the shuffled bin sequence (decoupled from slot).
        bin_frac = radial_bins[i]
        radial_t = 0.20 + 0.78 * bin_frac
        radial_t += rng.uniform(-0.05, 0.05)
        radial_t = max(0.18, min(1.0, radial_t))
        r_here = SPHERE_R * radial_t

        cx = r_here * math.sin(phi) * math.cos(theta)
        cy = r_here * math.sin(phi) * math.sin(theta)
        cz = r_here * math.cos(phi)
        color = EARTH_COLORS[i % len(EARTH_COLORS)]
        # Each constellation gets its own random rotation axis (unit vector)
        # and a slow rotation speed, so clusters spin INDEPENDENTLY of the
        # global camera. Sign of the speed varies so half spin clockwise,
        # half counter-clockwise.
        ax_phi = rng.uniform(0, math.pi)
        ax_theta = rng.uniform(0, 2 * math.pi)
        ax = math.sin(ax_phi) * math.cos(ax_theta)
        ay = math.sin(ax_phi) * math.sin(ax_theta)
        az = math.cos(ax_phi)
        spin_speed = (rng.uniform(0.05, 0.18)) * rng.choice([-1, 1])
        spin_phase = rng.uniform(0, 2 * math.pi)
        centres.append({
            "subject": subj,
            "x": round(cx, 2), "y": round(cy, 2), "z": round(cz, 2),
            "color": color,
            "origColor": color,
            "count": len(by_subject[subj]),
            "ax": round(ax, 3), "ay": round(ay, 3), "az": round(az, 3),
            "spinSpeed": round(spin_speed, 3),
            "spinPhase": round(spin_phase, 3),
        })

    # Place stars in a Gaussian-ish cloud around their subject centre.
    # Using a soft uniform-in-ball distribution with the centre's color.
    # Compute a size range across the whole library so star sizes scale with
    # book size (pages, or whatever proxy was provided). Books missing a
    # `pages` value get a neutral mid-range size. We normalize so the smallest
    # book in the library is ~0.7 and the largest is ~2.2; tiny random jitter
    # keeps same-sized stars from looking like clones.
    all_pages = [b.get("pages") for b in books if isinstance(b.get("pages"), (int, float)) and b["pages"] > 0]
    if all_pages:
        p_min = min(all_pages); p_max = max(all_pages)
    else:
        p_min = p_max = 0
    def size_from_pages(p):
        if not p or p_max == p_min:
            return rng.uniform(1.0, 1.4)          # neutral mid-range
        t = (p - p_min) / (p_max - p_min)         # 0..1
        base = 0.7 + t * 1.5                      # 0.7..2.2
        return base + rng.uniform(-0.08, 0.08)    # small jitter

    stars = []
    # remember which star indices belong to each constellation so we can wire
    # them up with intra-cluster synapses afterwards
    cluster_indices = []
    for ci, subj in enumerate(subjects):
        centre = centres[ci]
        idxs_here = []
        for b in by_subject[subj]:
            # random displacement inside a fuzzy ball: pick direction, then
            # radius weighted toward the centre with a soft falloff
            u = rng.uniform(-1, 1)
            theta = rng.uniform(0, 2 * math.pi)
            sqrt_1mu2 = math.sqrt(max(0, 1 - u * u))
            dx = math.cos(theta) * sqrt_1mu2
            dy = math.sin(theta) * sqrt_1mu2
            dz = u
            r = DRIFT * (rng.random() ** 1.3)    # higher power = stars pull tighter to centre
            ox = dx * r
            oy = dy * r
            oz = dz * r
            sx = centre["x"] + ox
            sy = centre["y"] + oy
            sz = centre["z"] + oz
            # mild per-star colour shift (saturation/lightness flicker)
            stars.append({
                "kind": "star",
                "title":    b.get("title", "Untitled"),
                "author":   b.get("author", "Unknown"),
                "year":     b.get("year", ""),
                "genre":    b.get("genre", ""),
                "subject":  subj,
                "subjects": b.get("subjects", []),
                "pages":    b.get("pages", 0),                # book size (pages or proxy)
                "x": round(sx, 2), "y": round(sy, 2), "z": round(sz, 2),
                # offset from its constellation centre (used live for gravity + rotation)
                "ox": round(ox, 2), "oy": round(oy, 2), "oz": round(oz, 2),
                "ci": ci,                                            # index into CENTRES
                "color": centre["color"],
                "origColor": centre["color"],
                "size":  round(size_from_pages(b.get("pages", 0)), 3),  # scaled by book size
                "phase": round(rng.uniform(0, 6.28), 3),     # twinkle phase
                "speed": round(rng.uniform(0.6, 1.6), 3),    # twinkle speed
            })
            idxs_here.append(len(stars) - 1)
        cluster_indices.append(idxs_here)

    # Synthesize dateAdded for the seed library. We spread the books across
    # the last ~5 years in order of their position in the build, so when the
    # user scrubs the time-lapse, the cosmos forms from a single star into
    # the full mind. The unit is milliseconds since epoch (matches JS Date.now).
    # Shuffle order is preserved by the build loop, which already gives us a
    # reasonable mix.
    import time as _time
    now_ms = int(_time.time() * 1000)
    five_years_ms = 5 * 365 * 24 * 60 * 60 * 1000
    n = len(stars)
    for i, st in enumerate(stars):
        # Older books at the start, newer at the end. We add a tiny per-book
        # jitter so they don't appear in perfect step.
        frac = (i + 1) / max(1, n)
        t = now_ms - int(five_years_ms * (1 - frac)) - int(rng.uniform(-3, 3) * 24 * 60 * 60 * 1000)
        st["dateAdded"] = t

    # Build the SYNAPSE web — always-visible, faint lines between stars in the
    # SAME constellation. Each star connects to its nearest neighbour in its
    # cluster, and (for larger clusters) to its next-nearest, giving a sparse
    # filigree that holds each constellation visibly together without
    # becoming a solid mesh.
    synapses = []
    for idxs in cluster_indices:
        m = len(idxs)
        if m < 2:
            continue
        for a_pos in range(m):
            a_idx = idxs[a_pos]
            a = stars[a_idx]
            # compute distances to every other star in this cluster
            dists = []
            for b_pos in range(m):
                if b_pos == a_pos: continue
                b_idx = idxs[b_pos]
                b = stars[b_idx]
                d2 = (a["x"]-b["x"])**2 + (a["y"]-b["y"])**2 + (a["z"]-b["z"])**2
                dists.append((d2, b_idx))
            dists.sort()
            # link to 1 nearest; in bigger clusters link to 2 (sparse web)
            k = 1 if m <= 3 else 2
            for d2, b_idx in dists[:k]:
                a_i, b_i = (a_idx, b_idx) if a_idx < b_idx else (b_idx, a_idx)
                # de-dupe via sorted pair key
                synapses.append({"a": a_i, "b": b_i})
    # remove duplicates
    seen = set(); uniq = []
    for s in synapses:
        k = (s["a"], s["b"])
        if k in seen: continue
        seen.add(k); uniq.append(s)
    synapses = uniq

    # Build the FULL connection graph between books that share any tag.
    # Stored once, used as a pool from which pulses are drawn at runtime.
    edges = []
    n = len(stars)
    for i in range(n):
        a = stars[i]
        a_subjects = set(s.lower() for s in (a.get("subjects") or []))
        a_genre    = (a.get("genre") or "").lower()
        a_author   = (a.get("author") or "").lower()
        for j in range(i + 1, n):
            b = stars[j]
            shared = False
            if a_subjects and a_subjects & set(s.lower() for s in (b.get("subjects") or [])):
                shared = True
            elif a_genre and a_genre == (b.get("genre") or "").lower():
                shared = True
            elif a_author and a_author == (b.get("author") or "").lower():
                shared = True
            if shared:
                edges.append({"a": i, "b": j})

    return {
        "stars": stars,
        "centres": centres,
        "edges": edges,
        "synapses": synapses,
        "subjects": subjects,
    }


def generate_html(mind):
    return TEMPLATE\
        .replace("__STARS__",   json.dumps(mind["stars"], ensure_ascii=False))\
        .replace("__CENTRES__", json.dumps(mind["centres"], ensure_ascii=False))\
        .replace("__EDGES__",   json.dumps(mind["edges"], ensure_ascii=False))\
        .replace("__SYNAPSES__", json.dumps(mind["synapses"], ensure_ascii=False))


def load_books(path):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    if isinstance(data, list): return data
    if isinstance(data, dict) and "books" in data: return data["books"]
    raise ValueError('JSON must be a list or {"books":[...]}')


def main():
    if len(sys.argv) > 1:
        path = sys.argv[1]
        if not os.path.exists(path):
            print(f"Error: file not found: {path}"); sys.exit(1)
        print(f"Loading library from {path}...")
        books = load_books(path)
    else:
        print(f"Loading demo library ({len(DEMO_BOOKS)} books)...")
        books = DEMO_BOOKS

    mind = build_mind(books)
    print(f"  -> {len(mind['stars'])} stars in {len(mind['centres'])} constellations")
    print(f"  -> {len(mind['edges'])} latent connections (pulses drawn from pool)")

    html = generate_html(mind)
    out_dir = os.path.dirname(os.path.abspath(__file__))
    out = os.path.join(out_dir, "neural_mind.html")
    with open(out, "w", encoding="utf-8") as f:
        f.write(html)

    # Write the PWA manifest, service worker, and icon alongside the HTML.
    # All three are required for the "Add to Home Screen" prompt and for the
    # app to feel installable. Upload all four files together when deploying.
    manifest = {
        "name": "Runaris",
        "short_name": "Runaris",
        "description": "A cosmos of every book you've ever read.",
        "start_url": "./neural_mind.html",
        "scope": "./",
        "display": "standalone",
        "orientation": "any",
        "background_color": "#F7F1E8",
        "theme_color": "#F7F1E8",
        "icons": [
            {"src": "./icon.svg", "sizes": "any", "type": "image/svg+xml", "purpose": "any"},
            {"src": "./icon.svg", "sizes": "any", "type": "image/svg+xml", "purpose": "maskable"},
        ],
    }
    with open(os.path.join(out_dir, "manifest.webmanifest"), "w", encoding="utf-8") as f:
        f.write(json.dumps(manifest, indent=2))

    # Minimal service worker — caches the HTML and core assets so the planetarium
    # opens offline. Covers and OpenLibrary queries still need network.
    sw_js = """// The Mind — service worker
const CACHE = 'runaris-v0.5.0';
const PRECACHE = ['./', './neural_mind.html', './manifest.webmanifest', './icon.svg'];

self.addEventListener('install', e => {
  e.waitUntil(caches.open(CACHE).then(c => c.addAll(PRECACHE)).then(() => self.skipWaiting()));
});
self.addEventListener('activate', e => {
  e.waitUntil(
    caches.keys().then(keys => Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});
// Cache-first for same-origin requests (the app shell). For cross-origin
// requests (cover images, OpenLibrary API), pass through to the network and
// don't cache — they're user-data adjacent.
self.addEventListener('fetch', e => {
  const url = new URL(e.request.url);
  if(url.origin !== self.location.origin) return;   // network as-is
  if(e.request.method !== 'GET') return;
  e.respondWith(
    caches.match(e.request).then(hit => hit || fetch(e.request).then(res => {
      // Cache only successful responses
      if(res && res.status === 200){
        const copy = res.clone();
        caches.open(CACHE).then(c => c.put(e.request, copy));
      }
      return res;
    }).catch(() => caches.match('./neural_mind.html')))
  );
});
"""
    with open(os.path.join(out_dir, "sw.js"), "w", encoding="utf-8") as f:
        f.write(sw_js)

    # SVG app icon — same glowing orb as the welcome screen, simplified for
    # icon use. Renders crisply at any size; works for home-screen install
    # on iOS and Android (Chrome will rasterize as needed).
    icon_svg = """<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512">
  <rect width="512" height="512" rx="112" fill="#F7F1E8"/>
  <g transform="translate(96 60) scale(3.4)">
    <path d="M44 30V92M44 30L74 36L70 56L44 60L76 92" stroke="#A5A79A" stroke-width="2.2" fill="none" stroke-linecap="round"/>
    <circle cx="44" cy="30" r="5" fill="#D4A93E"/><circle cx="74" cy="36" r="4" fill="#5A7340"/>
    <circle cx="70" cy="56" r="4" fill="#9A6C60"/><circle cx="44" cy="60" r="4.5" fill="#6F838C"/>
    <circle cx="44" cy="92" r="4" fill="#414B38"/><circle cx="76" cy="92" r="4" fill="#D4A93E"/>
  </g>
</svg>
"""
    with open(os.path.join(out_dir, "icon.svg"), "w", encoding="utf-8") as f:
        f.write(icon_svg)

    print(f"\n  Mind generated: {out}")
    print(f"  PWA files written: manifest.webmanifest, sw.js, icon.svg")
    print("  Opening in browser...")
    time.sleep(0.4)
    try:
        if sys.platform == "win32": os.startfile(out)
        elif sys.platform == "darwin": os.system(f'open "{out}"')
        else: webbrowser.open(f"file:///{out}")
    except Exception:
        print(f"\n  Open this file manually: {out}")
    print("\nControls:  Drag rotate  |  Scroll/pinch zoom  |  Tap star inspect")


TEMPLATE = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
<title>Runaris</title>
<!-- PWA: makes the page installable as a standalone app on Android/Chrome -->
<link rel="manifest" href="./manifest.webmanifest">
<meta name="theme-color" content="#F7F1E8">
<!-- iOS-specific: lets it install as an icon-on-home-screen app with no browser chrome -->
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="default">
<meta name="apple-mobile-web-app-title" content="Runaris">
<link rel="apple-touch-icon" href="./icon.svg">
<style>
  @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,500;1,500&family=Figtree:wght@400;500;600;700&display=swap');
  /* ── EARTH PALETTE TOKENS ─────────────────────────────────────────── */
  :root{
    --bg:#F7F1E8;        /* cream ground */
    --surface:#FDFAF4;   /* sheets, cards */
    --tint:#EBEDE0;      /* pale sage — hover, chips */
    --sage:#CFD0B0;      /* avatar */
    --line:#DDD4C6;      /* hairlines */
    --line-2:#A5A79A;    /* outline buttons */
    --ink:#2F3B4B;       /* deep navy text */
    --ink-2:#5C635B;     /* secondary text */
    --ink-3:#7A7F76;     /* placeholders */
    --forest:#414B38;    /* primary action */
    --olive:#5A7340;
    --mustard:#D4A93E;   /* add / accent */
    --clay:#9A6C60;
    --slate:#6F838C;
    --danger:#8C4A3C;
    --shadow:0 10px 30px rgba(47,59,75,0.12);
  }
  *,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
  html,body{width:100%;height:100%;background:var(--bg);overflow:hidden;font-family:'Figtree',sans-serif;color:var(--ink);touch-action:none;-webkit-font-smoothing:antialiased}
  button,input,select,textarea{font-family:inherit}
  #canvas{position:fixed;inset:0;width:100%;height:100%;display:block;cursor:grab}
  #canvas:active{cursor:grabbing}
  .sr-only{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap}

  /* ── HEADER ───────────────────────────────────────────────────────── */
  #hud{position:fixed;top:0;left:0;right:0;z-index:100;pointer-events:none;
       padding:calc(14px + env(safe-area-inset-top)) 20px 0;display:flex;flex-direction:column;gap:10px}
  .hud-row{display:flex;align-items:center;justify-content:space-between}
  .hud-title{font-family:'Cormorant Garamond',serif;font-size:30px;font-weight:500;letter-spacing:0.02em;color:var(--ink);pointer-events:auto}
  .profile-btn{pointer-events:auto;width:44px;height:44px;border-radius:22px;border:0;background:var(--sage);
       color:var(--forest);font-size:16px;font-weight:600;cursor:pointer;display:flex;align-items:center;justify-content:center}
  .profile-btn.guest{background:var(--tint);color:var(--ink-2)}
  .profile-btn:focus-visible,.nav-btn:focus-visible,.btn:focus-visible,.tt-btn:focus-visible{outline:2px solid var(--forest);outline-offset:2px}

  /* Search chip — only visible while a search is active (set from Library) */
  #hud-search{display:none;align-items:center;gap:6px;pointer-events:auto;align-self:flex-start;
       background:var(--surface);border:1px solid var(--line);border-radius:22px;padding:4px 4px 4px 14px;box-shadow:var(--shadow)}
  #hud-search.has-query{display:flex}
  #hud-search input{border:0;outline:0;background:transparent;color:var(--ink);font-size:14px;width:180px}
  #hud-search .x{width:36px;height:36px;border-radius:18px;display:flex;align-items:center;justify-content:center;
       font-size:20px;line-height:1;color:var(--ink-2);cursor:pointer;user-select:none}
  #hud-search .x:hover{background:var(--tint);color:var(--ink)}

  /* ── FILTER CHIPS (Settings → Visuals) ────────────────────────────── */
  .filter-chip-row{display:flex;flex-wrap:wrap;gap:8px}
  .filter-chip{font-size:13px;font-weight:500;padding:0 14px;height:36px;display:inline-flex;align-items:center;
       border-radius:18px;background:transparent;border:1px solid var(--line-2);color:var(--ink);cursor:pointer;user-select:none;transition:background .15s}
  .filter-chip:hover{background:var(--tint)}
  .filter-chip.active{background:var(--forest);border-color:var(--forest);color:var(--bg)}
  .filter-chip .dot{display:inline-block;width:8px;height:8px;border-radius:50%;margin-right:8px}
  .filter-chip .count{margin-left:8px;font-weight:600;opacity:0.7}

  /* ── CONNECTION-VIEW HINT ─────────────────────────────────────────── */
  #connect-hint{position:fixed;top:calc(72px + env(safe-area-inset-top));left:50%;transform:translateX(-50%) translateY(-8px);z-index:120;
       padding:10px 16px;background:var(--surface);border:1px solid var(--line);border-radius:22px;box-shadow:var(--shadow);
       opacity:0;pointer-events:none;transition:opacity .25s,transform .25s;font-size:13px;color:var(--ink-2);white-space:nowrap}
  #connect-hint.visible{opacity:1;transform:translateX(-50%) translateY(0);pointer-events:auto;cursor:pointer}
  #connect-hint .hl{color:var(--ink);font-weight:700;margin:0 3px}

  /* ── TOOLTIP: small card on hover, bottom sheet when a star is selected ── */
  #tooltip{position:fixed;z-index:500;pointer-events:none;opacity:0;transition:opacity .18s;max-width:260px}
  #tooltip.visible{opacity:1}
  .tooltip-inner{background:var(--surface);border:1px solid var(--line);border-radius:14px;box-shadow:var(--shadow);
       padding:12px 14px;position:relative;overflow:hidden;isolation:isolate}
  .tt-cover{position:absolute;inset:0;z-index:-2;background-size:cover;background-position:center;background-repeat:no-repeat;
       opacity:0;transition:opacity .55s ease-out;filter:blur(3px) saturate(0.7)}
  .tt-cover.loaded{opacity:0.28}
  .tooltip-inner::before{content:"";position:absolute;inset:0;z-index:-1;pointer-events:none;
       background:linear-gradient(135deg, rgba(253,250,244,0.72) 0%, rgba(253,250,244,0.94) 60%)}
  .tt-accent{display:none}
  .tt-kind{font-size:11px;font-weight:600;letter-spacing:0.12em;text-transform:uppercase;color:var(--slate);margin-bottom:4px}
  .tt-title{font-family:'Cormorant Garamond',serif;font-style:italic;font-size:19px;line-height:1.15;color:var(--ink);padding-right:28px;margin-bottom:2px}
  .tt-author{font-size:13px;color:var(--ink-2);margin-bottom:6px}
  .tt-tags{display:flex;flex-wrap:wrap;gap:6px}
  .tt-tag{font-size:11px;padding:3px 9px;border-radius:12px;background:var(--tint);color:var(--ink-2);border:0}
  .tt-tag.genre-tag{font-weight:600}

  #tooltip.pinned{pointer-events:auto;left:50% !important;top:auto !important;right:auto;
       bottom:calc(84px + env(safe-area-inset-bottom));transform:translateX(-50%);
       width:min(480px, calc(100vw - 24px));max-width:none}
  #tooltip.pinned .tooltip-inner{padding:18px 18px 16px;border-radius:20px}
  #tooltip.pinned .tt-title{font-size:26px;margin-bottom:4px}
  #tooltip.pinned .tt-author{font-size:15px;margin-bottom:10px}
  .tt-actions{display:flex;gap:10px;margin-top:14px}
  .tt-actions.hidden{display:none}
  .tt-btn{flex:1;height:48px;border-radius:24px;border:1px solid var(--line-2);background:transparent;color:var(--ink);
       font-size:15px;font-weight:600;cursor:pointer;transition:background .15s}
  .tt-btn:hover{background:var(--tint)}
  .tt-btn.primary{background:var(--forest);border-color:var(--forest);color:var(--bg)}
  .tt-btn.primary:hover{background:#353e2d}
  #tt-edit{flex:0 0 auto;padding:0 18px}
  #tt-dismiss{display:none}
  .tt-close{position:absolute;top:8px;right:8px;width:40px;height:40px;border-radius:20px;display:none;
       align-items:center;justify-content:center;font-size:22px;line-height:1;color:var(--ink-2);cursor:pointer}
  #tooltip.pinned .tt-close{display:flex}
  .tt-close:hover{background:var(--tint);color:var(--ink)}

  .tt-title-input,.tt-author-input{display:none;width:100%;background:#fff;border:1px solid var(--line);border-radius:10px;
       color:var(--ink);outline:none;margin-bottom:8px;padding:10px 12px}
  .tt-title-input{font-family:'Cormorant Garamond',serif;font-size:20px;font-style:italic}
  .tt-author-input{font-size:15px}
  .tt-title-input:focus,.tt-author-input:focus{border-color:var(--forest)}
  .tt-actions-edit{display:none;gap:10px;margin-top:10px}
  #tooltip.editing .tt-title,#tooltip.editing .tt-author,#tooltip.editing .tt-tags{display:none}
  #tooltip.editing .tt-title-input,#tooltip.editing .tt-author-input{display:block}
  #tooltip.editing #tt-actions{display:none}
  #tooltip.editing #tt-actions-edit{display:flex}

  /* ── BOOK DETAIL ──────────────────────────────────────────────────── */
  .book-hero{display:flex;gap:16px;align-items:flex-start;margin-bottom:16px}
  .book-orb{width:40px;height:40px;border-radius:50%;flex-shrink:0;background:currentColor}
  .book-cover-wrap{position:relative;width:88px;height:128px;flex-shrink:0;background:var(--tint);border-radius:8px;
       overflow:hidden;display:flex;align-items:center;justify-content:center}
  .book-cover-wrap .book-orb{transition:opacity .35s}
  .book-cover-wrap img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;opacity:0;transition:opacity .45s ease-out;display:block}
  .book-cover-wrap img.loaded{opacity:1}
  .book-cover-wrap.has-cover .book-orb{opacity:0}
  .book-cover-wrap .cover-spin{position:absolute;width:18px;height:18px;border-radius:50%;
       border:2px solid var(--line);border-top-color:var(--forest);animation:cover-spin .9s linear infinite;opacity:0;transition:opacity .2s}
  .book-cover-wrap.loading .cover-spin{opacity:1}
  @keyframes cover-spin{to{transform:rotate(360deg)}}
  .book-meta{flex:1}
  .book-meta .by{font-size:15px;color:var(--ink-2);margin-top:4px}
  .book-meta .yr{font-size:12px;letter-spacing:0.08em;color:var(--ink-2);text-transform:uppercase;margin-top:6px}
  .stars-row{display:flex;gap:4px;margin:8px 0 4px}
  .star-btn{font-size:24px;color:#CFC6B5;cursor:pointer;line-height:1;background:none;border:none;padding:4px;transition:color .12s}
  .star-btn.on,.star-btn:hover{color:var(--mustard)}
  .chip-row{display:flex;flex-wrap:wrap;gap:8px;margin-top:8px}
  .chip{font-size:13px;font-weight:500;padding:0 14px;height:36px;display:inline-flex;align-items:center;border-radius:18px;
       border:1px solid var(--line-2);color:var(--ink);cursor:pointer;transition:background .15s}
  .chip:hover{background:var(--tint)}
  .chip.active{background:var(--forest);border-color:var(--forest);color:var(--bg)}

  /* ── LIBRARY / INSIGHTS ───────────────────────────────────────────── */
  .insight-card{display:flex;align-items:center;gap:14px;padding:12px 14px;background:var(--surface);
       border:1px solid var(--line);border-radius:14px;margin-bottom:8px;cursor:pointer;transition:background .15s}
  .insight-card:hover{background:var(--tint)}
  .insight-ico{width:12px;height:12px;border-radius:50%;flex-shrink:0;background:currentColor}
  .insight-body{flex:1;min-width:0}
  .insight-label{font-size:11px;font-weight:600;letter-spacing:0.1em;text-transform:uppercase;color:var(--ink-2);margin-bottom:2px}
  .insight-value{font-family:'Cormorant Garamond',serif;font-style:italic;font-size:19px;color:var(--ink);white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
  .insight-meta{font-size:13px;color:var(--ink-2);margin-top:2px}
  .insight-card.empty{cursor:default;opacity:0.6}
  .insight-card.empty:hover{background:var(--surface)}
  .lib-search{width:100%;height:48px;border-radius:24px;border:1px solid var(--line);background:#fff;padding:0 18px;
       font-size:15px;color:var(--ink);outline:none;margin-bottom:14px}
  .lib-search:focus{border-color:var(--forest)}
  .lib-row{display:flex;align-items:center;gap:12px;width:100%;min-height:52px;padding:8px 4px;border:0;border-bottom:1px solid var(--line);
       background:transparent;text-align:left;cursor:pointer;color:var(--ink)}
  .lib-row:hover{background:var(--tint)}
  .lib-dot{width:10px;height:10px;border-radius:50%;flex-shrink:0}
  .lib-t{font-family:'Cormorant Garamond',serif;font-style:italic;font-size:18px;line-height:1.15}
  .lib-a{font-size:13px;color:var(--ink-2)}

  /* ── BARCODE SCANNER (camera stays dark for contrast) ─────────────── */
  #scanner{position:fixed;inset:0;z-index:450;display:none;align-items:center;justify-content:center;background:#1d2229;flex-direction:column}
  #scanner.open{display:flex}
  #scanner video{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;background:#1d2229}
  #scanner .reticle{position:relative;width:min(82vw,520px);aspect-ratio:2/1;border:2px solid var(--bg);border-radius:14px;
       box-shadow:0 0 0 9999px rgba(29,34,41,0.45);pointer-events:none}
  #scanner .sweep{position:absolute;left:8px;right:8px;height:2px;background:var(--mustard);border-radius:1px;
       animation:scan-sweep 1.8s linear infinite;pointer-events:none;top:0}
  @keyframes scan-sweep{0%{top:8%}50%{top:92%}100%{top:8%}}
  #scanner .scanner-hint,#scanner .scanner-status,.scanner-batch{position:absolute;left:50%;transform:translateX(-50%);z-index:2;
       background:var(--surface);color:var(--ink);border-radius:22px;padding:10px 16px;font-size:14px;box-shadow:var(--shadow);
       white-space:nowrap;max-width:90vw;text-align:center}
  #scanner .scanner-hint{top:calc(20px + env(safe-area-inset-top))}
  #scanner .scanner-status{bottom:96px;font-weight:600;min-width:200px}
  #scanner .scanner-status.error{color:var(--danger)}
  #scanner .scanner-close{position:absolute;top:calc(72px + env(safe-area-inset-top));right:16px;z-index:2;height:44px;padding:0 18px;
       border-radius:22px;border:0;background:var(--surface);color:var(--ink);font-size:14px;font-weight:600;cursor:pointer}
  .scanner-batch{bottom:32px;display:flex;align-items:center;gap:8px;cursor:pointer;user-select:none;font-weight:500}
  .scanner-batch input{accent-color:var(--forest);width:18px;height:18px;cursor:pointer}

  /* ── SCAN PREVIEW ─────────────────────────────────────────────────── */
  #scan-preview{position:fixed;inset:0;z-index:460;display:none;align-items:center;justify-content:center;
       background:rgba(47,59,75,0.3);backdrop-filter:blur(4px);padding:16px}
  #scan-preview.open{display:flex}
  #scan-preview .preview-card{width:min(420px,100%);background:var(--surface);border-radius:20px;box-shadow:var(--shadow);padding:20px}
  #scan-preview .preview-row{display:flex;gap:16px;margin-bottom:18px}
  #scan-preview .preview-cover{width:88px;height:128px;flex-shrink:0;background:var(--tint);border-radius:8px;
       background-size:cover;background-position:center;background-repeat:no-repeat;position:relative;overflow:hidden}
  #scan-preview .preview-cover.empty::after{content:"No cover";position:absolute;inset:0;display:flex;align-items:center;justify-content:center;
       font-size:12px;color:var(--ink-2)}
  #scan-preview .preview-body{flex:1;min-width:0}
  #scan-preview .preview-title{font-family:'Cormorant Garamond',serif;font-style:italic;font-size:22px;color:var(--ink);line-height:1.15;margin-bottom:4px}
  #scan-preview .preview-author{font-size:15px;color:var(--ink-2);margin-bottom:4px}
  #scan-preview .preview-meta{font-size:12px;letter-spacing:0.06em;color:var(--ink-2);text-transform:uppercase}
  #scan-preview .preview-isbn{font-size:12px;color:var(--ink-2);margin-top:6px}

  /* ── FIRST-LAUNCH WELCOME ─────────────────────────────────────────── */
  #welcome{position:fixed;inset:0;z-index:700;display:none;align-items:center;justify-content:center;background:var(--bg);padding:20px}
  #welcome.open{display:flex}
  .welcome-card{width:min(460px,100%);max-height:94vh;overflow-y:auto;text-align:center}
  .welcome-orb{width:72px;height:72px;margin:0 auto 12px;display:block}
  .welcome-title{font-family:'Cormorant Garamond',serif;font-weight:500;font-size:44px;color:var(--ink);margin-bottom:6px}
  .welcome-tag{font-family:'Cormorant Garamond',serif;font-style:italic;font-size:19px;line-height:1.4;color:var(--ink-2);margin-bottom:28px}
  .welcome-doors{display:grid;gap:10px;text-align:left}
  .welcome-door{display:flex;align-items:center;gap:14px;padding:14px 16px;background:var(--surface);border:1px solid var(--line);
       border-radius:16px;cursor:pointer;transition:background .15s}
  .welcome-door:hover{background:var(--tint)}
  .welcome-door.primary{background:var(--forest);border-color:var(--forest)}
  .welcome-door.primary .welcome-door-title,.welcome-door.primary .welcome-door-sub{color:var(--bg)}
  .welcome-door.primary .welcome-door-ico{background:rgba(247,241,232,0.16);color:var(--bg)}
  .welcome-door-ico{width:40px;height:40px;flex-shrink:0;display:flex;align-items:center;justify-content:center;
       font-size:18px;border-radius:20px;background:var(--tint);color:var(--forest)}
  .welcome-door-body{flex:1;min-width:0}
  .welcome-door-title{font-size:16px;font-weight:600;color:var(--ink);margin-bottom:2px}
  .welcome-door-sub{font-size:13px;color:var(--ink-2);line-height:1.4}
  .welcome-footer{margin-top:22px;font-size:14px;color:var(--ink-2)}
  .welcome-footer a{color:var(--forest);font-weight:600;cursor:pointer;text-decoration:underline;text-underline-offset:3px}

  /* ── TIME-LAPSE ───────────────────────────────────────────────────── */
  #timelapse{position:fixed;left:50%;transform:translateX(-50%) translateY(12px);bottom:calc(84px + env(safe-area-inset-bottom));z-index:310;
       padding:14px 16px;background:var(--surface);border:1px solid var(--line);border-radius:20px;box-shadow:var(--shadow);
       width:min(480px, calc(100vw - 24px));display:none;flex-direction:column;gap:10px;opacity:0;transition:opacity .25s,transform .25s}
  #timelapse.open{display:flex;opacity:1;transform:translateX(-50%) translateY(0)}
  #timelapse .tl-row{display:flex;align-items:center;gap:10px}
  #timelapse .tl-label{font-size:11px;font-weight:600;letter-spacing:0.1em;text-transform:uppercase;color:var(--ink-2)}
  #timelapse .tl-date{font-family:'Cormorant Garamond',serif;font-style:italic;font-size:20px;color:var(--ink);flex:1;text-align:center}
  #timelapse .tl-count{font-size:13px;color:var(--ink-2);text-align:right;min-width:70px}
  #timelapse input[type=range]{width:100%;accent-color:var(--forest)}
  #timelapse .tl-controls{display:flex;align-items:center;gap:8px}
  #timelapse .tl-btn{height:40px;padding:0 16px;border-radius:20px;border:1px solid var(--line-2);background:transparent;color:var(--ink);
       font-size:14px;font-weight:600;cursor:pointer}
  #timelapse .tl-btn:hover{background:var(--tint)}
  #timelapse .tl-btn.primary{background:var(--forest);border-color:var(--forest);color:var(--bg)}
  #timelapse .tl-close{width:36px;height:36px;border-radius:18px;display:flex;align-items:center;justify-content:center;
       font-size:22px;line-height:1;color:var(--ink-2);cursor:pointer}
  #timelapse .tl-close:hover{background:var(--tint)}

  /* ── BOTTOM NAV ───────────────────────────────────────────────────── */
  #dock{position:fixed;left:0;right:0;bottom:0;z-index:420;display:flex;align-items:center;justify-content:space-between;
       padding:10px 20px calc(12px + env(safe-area-inset-bottom));background:var(--bg);border-top:1px solid var(--line)}
  .nav-btn{min-width:88px;height:44px;border:0;background:transparent;border-radius:22px;cursor:pointer;
       font-size:15px;font-weight:500;color:var(--ink-2)}
  .nav-btn:hover{background:var(--tint)}
  .nav-btn.active{color:var(--ink);font-weight:700}
  .nav-add{width:48px;height:48px;min-width:0;border-radius:24px;background:var(--mustard);color:var(--ink);
       display:flex;align-items:center;justify-content:center}
  .nav-add:hover{background:#c69b30}

  /* ── MODAL ────────────────────────────────────────────────────────── */
  #modal{position:fixed;inset:0;z-index:400;display:none;align-items:center;justify-content:center;
       background:rgba(47,59,75,0.28);backdrop-filter:blur(4px)}
  #modal.open{display:flex}
  .panel{width:min(540px,92vw);max-height:88vh;overflow:hidden;display:flex;flex-direction:column;
       background:var(--surface);border-radius:20px;box-shadow:var(--shadow)}
  .panel-head{display:flex;align-items:center;justify-content:space-between;padding:16px 16px 8px 20px}
  .panel-title{font-family:'Cormorant Garamond',serif;font-weight:500;font-size:28px;color:var(--ink)}
  .panel-close{width:44px;height:44px;border-radius:22px;display:flex;align-items:center;justify-content:center;
       font-size:24px;color:var(--ink-2);cursor:pointer;line-height:1}
  .panel-close:hover{background:var(--tint);color:var(--ink)}
  .panel-body{padding:12px 20px 24px;overflow-y:auto;flex:1}
  .panel-tabs{display:flex;gap:4px;padding:0 12px;border-bottom:1px solid var(--line);overflow-x:auto}
  .panel-tabs:empty{display:none}
  .panel-tab{padding:12px 10px;font-size:14px;font-weight:500;color:var(--ink-2);cursor:pointer;border-bottom:2px solid transparent;white-space:nowrap}
  .panel-tab:hover{color:var(--ink)}
  .panel-tab.active{color:var(--ink);font-weight:700;border-bottom-color:var(--forest)}
  @media (max-width:560px){
    /* Sheet rises from just above the nav, so Cosmos / Library / + stay reachable */
    #modal{align-items:flex-end;padding-bottom:calc(71px + env(safe-area-inset-bottom))}
    .panel{width:100%;max-height:calc(100% - 16px);border-radius:20px 20px 0 0}
  }

  /* ── FORMS ────────────────────────────────────────────────────────── */
  .field{margin-bottom:14px}
  .field label{display:block;font-size:12px;font-weight:600;letter-spacing:0.08em;text-transform:uppercase;color:var(--ink-2);margin-bottom:6px}
  .field input[type=text],.field input[type=email],.field input[type=password],.field input[type=date],.field textarea,.field select{
       width:100%;background:#fff;border:1px solid var(--line);border-radius:10px;color:var(--ink);font-size:15px;
       padding:11px 12px;outline:none;transition:border-color .2s}
  .field input:focus,.field textarea:focus,.field select:focus{border-color:var(--forest)}
  .field input::placeholder,.field textarea::placeholder{color:var(--ink-3)}
  .field textarea{min-height:90px;resize:vertical}
  .field-row{display:flex;gap:10px}
  .field-row .field{flex:1;min-width:0}
  .field input[type=range]{width:100%;accent-color:var(--forest)}
  .field input[type=checkbox]{accent-color:var(--forest);width:18px;height:18px;margin-right:8px;vertical-align:-3px}
  .range-row{display:flex;justify-content:space-between;align-items:center;margin-bottom:4px}
  .range-row label{margin-bottom:0}
  .range-row b{color:var(--ink);font-size:14px}
  .btn{display:inline-flex;align-items:center;justify-content:center;gap:8px;min-height:44px;padding:0 20px;font-size:15px;font-weight:600;
       border:1px solid var(--line-2);border-radius:22px;background:transparent;color:var(--ink);cursor:pointer;transition:background .15s;margin:0 6px 6px 0}
  .btn:hover{background:var(--tint)}
  .btn:disabled{opacity:0.5;cursor:default}
  .btn-primary{background:var(--forest);border-color:var(--forest);color:var(--bg)}
  .btn-primary:hover{background:#353e2d}
  .btn-danger{border-color:var(--danger);color:var(--danger)}
  .btn-danger:hover{background:#f3e3dd}
  .btn-block{display:flex;width:100%;justify-content:flex-start;margin:0 0 8px;border-radius:12px}

  .oauth-btn{display:flex;align-items:center;gap:12px;width:100%;min-height:48px;padding:0 16px;background:#fff;border:1px solid var(--line);
       border-radius:12px;color:var(--ink);font-size:15px;font-weight:500;cursor:pointer;margin-bottom:8px}
  .oauth-btn:hover{background:var(--tint)}
  .oauth-ico{width:24px;height:24px;flex-shrink:0;display:flex;align-items:center;justify-content:center;font-weight:700;border-radius:6px;font-size:13px}
  .oauth-google .oauth-ico{background:var(--tint);color:var(--ink)}
  .oauth-apple .oauth-ico{background:var(--ink);color:var(--bg)}
  .oauth-email .oauth-ico{background:var(--sage);color:var(--forest)}
  .divider{display:flex;align-items:center;gap:10px;margin:16px 0;font-size:12px;letter-spacing:0.08em;text-transform:uppercase;color:var(--ink-2)}
  .divider::before,.divider::after{content:"";flex:1;height:1px;background:var(--line)}

  .service-tile{display:flex;align-items:center;gap:12px;min-height:56px;padding:8px 14px;background:#fff;border:1px solid var(--line);
       border-radius:12px;margin-bottom:8px;cursor:pointer}
  .service-tile:hover{background:var(--tint)}
  .service-tile .ico{width:36px;height:36px;border-radius:8px;display:flex;align-items:center;justify-content:center;font-weight:700;font-size:13px;flex-shrink:0}
  .service-tile .name{flex:1;font-size:15px;font-weight:500}
  .service-tile .status{font-size:12px;font-weight:600;color:var(--ink-2)}
  .service-tile.connected .status{color:var(--olive)}
  .service-tile.connected{border-color:var(--olive)}

  .help{font-size:14px;color:var(--ink-2);line-height:1.5;margin-top:6px}
  .help code{background:var(--tint);padding:1px 6px;border-radius:4px;font-size:13px;color:var(--ink)}
  .section-title{font-size:12px;font-weight:600;letter-spacing:0.1em;text-transform:uppercase;color:var(--ink-2);margin:22px 0 10px}
  .section-title:first-child{margin-top:4px}
  .stat-num{font-family:'Cormorant Garamond',serif;font-size:32px;line-height:1;color:var(--ink)}

  /* ── TOAST ────────────────────────────────────────────────────────── */
  #toast{position:fixed;bottom:calc(88px + env(safe-area-inset-bottom));left:50%;transform:translateX(-50%) translateY(12px);z-index:600;
       background:var(--ink);color:var(--bg);border-radius:22px;padding:12px 18px;font-size:14px;font-weight:500;
       opacity:0;pointer-events:none;transition:opacity .25s,transform .25s;max-width:calc(100vw - 32px)}
  #toast.show{opacity:1;transform:translateX(-50%) translateY(0)}
</style>
</head>
<body>
<canvas id="canvas"></canvas>

<div id="hud">
  <div class="hud-row">
    <div class="hud-title">Runaris</div>
    <button class="profile-btn guest" id="dock-profile" data-action="profile" aria-label="Profile and settings">
      <span id="avatar-letter" aria-hidden="true">?</span><span class="sr-only" id="profile-name">Sign in</span>
    </button>
  </div>
  <div id="hud-search">
    <input type="text" id="hud-search-input" placeholder="Search" aria-label="Search your library">
    <div class="x" id="hud-search-clear" role="button" aria-label="Clear search">×</div>
  </div>
</div>

<!-- ── CONNECTION-VIEW HINT (only when active) ────────────────────── -->
<div id="connect-hint">
  Showing <span class="hl" id="connect-count">0</span> connections · tap empty space to exit
</div>

<div id="tooltip"><div class="tooltip-inner">
  <div class="tt-cover" id="tt-cover"></div>
  <div class="tt-accent" id="tt-accent"></div>
  <div class="tt-close" id="tt-close" role="button" aria-label="Close">×</div>
  <div class="tt-kind" id="tt-kind"></div>
  <div class="tt-title" id="tt-title"></div>
  <input class="tt-title-input" id="tt-title-input" type="text" placeholder="Title" autocomplete="off" spellcheck="false">
  <div class="tt-author" id="tt-author"></div>
  <input class="tt-author-input" id="tt-author-input" type="text" placeholder="Author" autocomplete="off" spellcheck="false">
  <div class="tt-tags" id="tt-tags"></div>
  <div class="tt-actions hidden" id="tt-actions">
    <button class="tt-btn primary" id="tt-expand">Open</button>
    <button class="tt-btn" id="tt-connect">Connections</button>
    <button class="tt-btn" id="tt-edit">Edit</button>
    <button class="tt-btn" id="tt-dismiss">Dismiss</button>
  </div>
  <div class="tt-actions-edit" id="tt-actions-edit">
    <button class="tt-btn primary" id="tt-save">Save</button>
    <button class="tt-btn" id="tt-cancel">Cancel</button>
  </div>
</div></div>

<!-- ── BOTTOM NAV ─────────────────────────────────────────────────── -->
<nav id="dock" aria-label="Main">
  <button class="nav-btn active" data-action="cosmos" id="nav-cosmos">Cosmos</button>
  <button class="nav-btn" data-action="library" id="nav-library">Library</button>
  <button class="nav-btn nav-add" data-action="add-book" aria-label="Add a book">
    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" aria-hidden="true"><path d="M12 5v14M5 12h14"/></svg>
  </button>
</nav>

<!-- ── FIRST-LAUNCH WELCOME ─────────────────────────────────────────── -->
<div id="welcome">
  <div class="welcome-card">
    <svg class="welcome-orb" viewBox="30 18 58 84" aria-hidden="true"><path d="M44 30V92M44 30L74 36L70 56L44 60L76 92" stroke="#A5A79A" stroke-width="2.4" fill="none" stroke-linecap="round"/><circle cx="44" cy="30" r="5" fill="#D4A93E"/><circle cx="74" cy="36" r="4" fill="#5A7340"/><circle cx="70" cy="56" r="4" fill="#9A6C60"/><circle cx="44" cy="60" r="4.5" fill="#6F838C"/><circle cx="44" cy="92" r="4" fill="#414B38"/><circle cx="76" cy="92" r="4" fill="#D4A93E"/></svg>
    <div class="welcome-title">Runaris</div>
    <div class="welcome-tag">A cosmos of everything you've ever read.<br>Each book is a star. Each subject a constellation.</div>
    <div class="welcome-doors">
      <div class="welcome-door primary" data-door="scan">
        <div class="welcome-door-ico"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M4 7V4h3M17 4h3v3M20 17v3h-3M7 20H4v-3M8 8v8M12 8v8M16 8v8"/></svg></div>
        <div class="welcome-door-body">
          <div class="welcome-door-title">Scan a book to start</div>
          <div class="welcome-door-sub">Point your camera at any back-cover barcode</div>
        </div>
      </div>
      <div class="welcome-door" data-door="import">
        <div class="welcome-door-ico">⇪</div>
        <div class="welcome-door-body">
          <div class="welcome-door-title">Import my library</div>
          <div class="welcome-door-sub">CSV or JSON · Goodreads, StoryGraph, or your own</div>
        </div>
      </div>
      <div class="welcome-door" data-door="add">
        <div class="welcome-door-ico">+</div>
        <div class="welcome-door-body">
          <div class="welcome-door-title">Add a book manually</div>
          <div class="welcome-door-sub">Type a title and author, build your mind one book at a time</div>
        </div>
      </div>
      <div class="welcome-door" data-door="explore">
        <div class="welcome-door-ico">✦</div>
        <div class="welcome-door-body">
          <div class="welcome-door-title">Explore the demo first</div>
          <div class="welcome-door-sub">Wander a sample library before adding your own</div>
        </div>
      </div>
    </div>
    <div class="welcome-footer">
      Or <a id="welcome-signin">sign in</a> to sync across devices
    </div>
  </div>
</div>

<!-- ── BARCODE SCANNER OVERLAY ──────────────────────────────────────── -->
<div id="scanner">
  <video id="scanner-video" playsinline muted autoplay></video>
  <div class="scanner-hint">Aim the camera at the back-cover barcode</div>
  <button class="scanner-close" id="scanner-close">Cancel</button>
  <div class="reticle"><div class="sweep"></div></div>
  <div class="scanner-status" id="scanner-status">Initializing camera…</div>
  <label class="scanner-batch" id="scanner-batch-label">
    <input type="checkbox" id="scanner-batch"> <span>Batch mode · keep scanning</span>
  </label>
</div>

<!-- ── SCAN PREVIEW (confirmation card) ─────────────────────────────── -->
<div id="scan-preview">
  <div class="preview-card">
    <div class="preview-row">
      <div class="preview-cover" id="preview-cover"></div>
      <div class="preview-body">
        <div class="preview-title" id="preview-title">Looking up…</div>
        <div class="preview-author" id="preview-author"></div>
        <div class="preview-meta" id="preview-meta"></div>
        <div class="preview-isbn" id="preview-isbn"></div>
      </div>
    </div>
    <div style="display:flex;gap:0.5rem">
      <button class="btn btn-primary" id="preview-add" style="flex:1">Add to mind</button>
      <button class="btn" id="preview-rescan">Scan another</button>
      <button class="btn" id="preview-cancel">Cancel</button>
    </div>
  </div>
</div>

<!-- ── TIME-LAPSE PANEL (toggleable) ───────────────────────────────── -->
<div id="timelapse">
  <div class="tl-row">
    <span class="tl-label">Time-lapse</span>
    <span class="tl-date" id="tl-date">—</span>
    <span class="tl-count" id="tl-count">0 books</span>
    <span class="tl-close" id="tl-close">×</span>
  </div>
  <input type="range" id="tl-slider" min="0" max="1000" step="1" value="1000">
  <div class="tl-controls">
    <button class="tl-btn primary" id="tl-play">▶ Play</button>
    <button class="tl-btn" id="tl-reset">Now</button>
    <span style="flex:1"></span>
    <span class="tl-label">Drag the slider to scrub through time</span>
  </div>
</div>

<!-- ── MODAL PANEL ───────────────────────────────────────────────────── -->
<div id="modal">
  <div class="panel">
    <div class="panel-head">
      <div class="panel-title" id="modal-title">Settings</div>
      <div class="panel-close" id="modal-close">×</div>
    </div>
    <div class="panel-tabs" id="modal-tabs"></div>
    <div class="panel-body" id="modal-body"></div>
  </div>
</div>

<!-- ── TOAST ─────────────────────────────────────────────────────────── -->
<div id="toast"></div>

<script>
const STARS    = __STARS__;
const CENTRES  = __CENTRES__;
const EDGES    = __EDGES__;
const SYNAPSES = __SYNAPSES__;

// ── APP STATE (in-memory only) ──────────────────────────────────────────
// Declared early so the draw loop and any other initialisation code that
// references `app` can safely read it from frame 1. (const has a temporal
// dead zone — defining this lower in the file would crash draw().)
const app = {
  user: null,                       // {name,email,avatar} when "signed in"
  frozen: false,                    // when a star is focused, all motion pauses
  bookData: {},                     // per-book {notes, rating, status} keyed by makeBookKey
  statusFilter: 'all',              // all | reading | finished | unread | abandoned
  searchQuery: '',                  // live search (not persisted)
  timelapseAt: null,                // when scrubbing time: ms-since-epoch cutoff; null = present
  welcomed: false,                  // first-launch flag — set true once the user dismisses welcome
  connectMode: null,                // when showing connections: { sourceIdx, lit:Set<int> }
  connections: {                    // visual-only toggles
    goodreads: false, storygraph: false, kindle: false, librarything: false,
  },
  visual: {                         // live customisation, applied each frame
    pulseRate: 1.0,                 // multiplier on spawn rate
    breathing: true,                // toggle sphere breath
    nebula: true,                   // toggle global cloud
    synapses: true,                 // toggle in-cluster synapse threads
    starBrightness: 1.0,            // multiplier on star size
    rotationSpeed: 0.0,             // auto-rotate around vertical (rad/sec)
    paletteMode: 'default',         // default | warm | cool | mono
    gravity: 1.0,                   // tightness of constellations (0.3 loose .. 2.0 tight)
    nebulaOpacity: 1.0,             // multiplier on nebula wisp alpha
    nebulaColor: 'auto',            // auto | blue | violet | teal | amber | rose | mono | custom
    nebulaCustom: '#8E7F78',        // used when nebulaColor === 'custom'
    constellationSpin: 1.0,         // multiplier on each centre's own spin speed
    showLabels: true,               // constellation labels (italic names over each cluster)
  },
};

// ── PERSISTENCE ─────────────────────────────────────────────────────────
// Save/restore via localStorage so the mindmap survives reloads. We persist
// the parts of `app` that users can change (visual settings, user/social
// shells, bookData with notes/ratings/status) and the library mutations
// (added/removed stars). The original demo data is the seed — once the
// user has changed anything, their saved state takes over.
const STORAGE_KEY = 'neuralMind.v1';
// Earth palette — one colour per constellation, cycled. Mirrors EARTH_COLORS in Python.
const EARTH_COLORS = ['#5A7340','#9A6C60','#6F838C','#D4A93E','#414B38','#8E7F78','#5F6C78','#B99D84','#5A3A2C','#7A8078','#4D6142','#898270'];
const THEME_VERSION = 2;
const APP_VERSION = '0.5.0';
// Where feedback emails go. EDIT THIS to your real address.
const FEEDBACK_EMAIL = 'feedback@themind.app';
let _saveTimer = null;

function saveState(){
  if(_saveTimer) clearTimeout(_saveTimer);
  _saveTimer = setTimeout(() => {
    try {
      const data = {
        bookData:     app.bookData,
        user:         app.user,
        connections:  app.connections,
        visual:       app.visual,
        statusFilter: app.statusFilter,
        welcomed:     app.welcomed,
        themeV:       THEME_VERSION,
        // Library snapshot — strip render-only fields so the saved blob is small.
        stars: STARS.map(s => ({
          title:s.title, author:s.author, year:s.year, genre:s.genre,
          subject:s.subject, subjects:s.subjects, pages:s.pages,
          x:s.x, y:s.y, z:s.z, ox:s.ox, oy:s.oy, oz:s.oz, ci:s.ci,
          color:s.color, origColor:s.origColor, size:s.size, phase:s.phase, speed:s.speed,
          dateAdded:s.dateAdded,
        })),
        centres: CENTRES.map(c => ({
          subject:c.subject, x:c.x, y:c.y, z:c.z, color:c.color, origColor:c.origColor, count:c.count,
          ax:c.ax, ay:c.ay, az:c.az, spinSpeed:c.spinSpeed, spinPhase:c.spinPhase,
        })),
        edges: EDGES, synapses: SYNAPSES,
      };
      localStorage.setItem(STORAGE_KEY, JSON.stringify(data));
    } catch(e){ /* quota or disabled — fail quietly */ }
  }, 400);
}

function loadState(){
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if(!raw) return false;
    const d = JSON.parse(raw);
    if(d.bookData)     Object.assign(app.bookData, d.bookData);
    if(d.user)         app.user = d.user;
    if(d.connections)  Object.assign(app.connections, d.connections);
    if(d.visual)       Object.assign(app.visual, d.visual);
    if(d.statusFilter) app.statusFilter = d.statusFilter;
    if(typeof d.welcomed === 'boolean') app.welcomed = d.welcomed;
    // Replace library arrays in place (don't reassign — other code holds refs)
    if(Array.isArray(d.stars)   && d.stars.length)  { STARS.length=0;   for(const s of d.stars)    STARS.push(s); }
    if(Array.isArray(d.centres) && d.centres.length){ CENTRES.length=0; for(const c of d.centres)  CENTRES.push(c); }
    if(Array.isArray(d.edges))   { EDGES.length=0;    for(const e of d.edges)     EDGES.push(e); }
    if(Array.isArray(d.synapses)){ SYNAPSES.length=0; for(const s of d.synapses)  SYNAPSES.push(s); }
    // Libraries saved under the old dark theme carry neon colours: repaint
    // them once in the earth palette (by constellation) and reset nebula tint.
    if(d.themeV !== THEME_VERSION){
      CENTRES.forEach((c, i) => { c.color = c.origColor = EARTH_COLORS[i % EARTH_COLORS.length]; });
      STARS.forEach(s => {
        const c = CENTRES[s.ci];
        s.color = s.origColor = c ? c.color : EARTH_COLORS[0];
      });
      app.visual.nebulaCustom = '#8E7F78';
      app.visual.paletteMode = 'default';
    }
    return true;
  } catch(e){ return false; }
}

function clearPersistedState(){
  try { localStorage.removeItem(STORAGE_KEY); } catch(e){}
}

// Apply saved state immediately — must happen before draw() runs.
const _loaded = loadState();

// ── BOOK STATUS LOOKUPS ─────────────────────────────────────────────────
// Declared early so draw() can read them on frame 1 without hitting a TDZ.
// `bookData` is the read/write accessor (used by the detail panel); this
// peek-version is read-only and used every frame.
function makeBookKey(s){ return (s.title || '') + '||' + (s.author || ''); }
function peekStatus(s){
  const d = app.bookData[makeBookKey(s)];
  return (d && d.status) || 'unread';
}
// Search match — case-insensitive substring across title, author, subjects.
function starMatchesSearch(s, q){
  if(!q) return true;
  q = String(q).toLowerCase();
  if((s.title || '').toLowerCase().includes(q))  return true;
  if((s.author || '').toLowerCase().includes(q)) return true;
  if((s.genre || '').toLowerCase().includes(q))  return true;
  for(const t of (s.subjects || [])){
    if(String(t).toLowerCase().includes(q)) return true;
  }
  return false;
}
const STATUS_STYLES = {
  unread:    null,                                            // no ring
  reading:   { color: '#2F3B4B', style: 'solid' },            // solid ring
  finished:  { color: '#5A7340', style: 'solid-dot' },        // ring + inner dot
  abandoned: { color: '#8E7F78', style: 'dashed' },           // dashed ring
};

// ── CANVAS ────────────────────────────────────────────────────────────────
const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d');
let W, H, DPR;
function resize(){
  DPR = Math.min(window.devicePixelRatio || 1, 2);
  W = canvas.width  = innerWidth  * DPR;
  H = canvas.height = innerHeight * DPR;
  canvas.style.width  = innerWidth  + 'px';
  canvas.style.height = innerHeight + 'px';
}
resize();
addEventListener('resize', resize);

// ── CAMERA ────────────────────────────────────────────────────────────────
// Two-axis orbit camera: rotY around vertical, rotX up/down. Drag to look around.
const cam = { rotX: 0.18, rotY: 0.55, dist: 1500, scale: 1.0 };
function project(x, y, z){
  // rotate around Y (azimuth)
  const cy = Math.cos(cam.rotY), sy = Math.sin(cam.rotY);
  let rx = x * cy - z * sy;
  let rz = x * sy + z * cy;
  // rotate around X (elevation)
  const cx = Math.cos(cam.rotX), sx = Math.sin(cam.rotX);
  let ry  = y * cx - rz * sx;
  let rz2 = y * sx + rz * cx;
  // perspective
  const persp = cam.dist / Math.max(cam.dist + rz2, 1);
  return {
    sx: W * 0.5 + rx * persp * cam.scale,
    sy: H * 0.5 + ry * persp * cam.scale,
    persp,
    depth: rz2,
  };
}

function fitView(){
  cam.scale = 1.0;
  // make sure the whole sphere is comfortably visible
  let maxR = 1;
  for(const s of STARS){ const r = Math.hypot(s.x, s.y, s.z); if(r > maxR) maxR = r; }
  const margin = Math.min(W, H) * 0.40;
  // approximate projected radius: just use maxR since the sphere is roughly isotropic
  cam.scale = margin / maxR;
}
fitView();

// ── BREATHING ─────────────────────────────────────────────────────────────
// The whole mind expands and contracts slowly. Two layered breaths give a
// non-mechanical "alive" feel: slow deep breath + fast subtle pulse.
function breathScale(t){
  return 1 + Math.sin(t * 0.5)  * 0.045   // ~12 s deep breath
           + Math.sin(t * 1.7)  * 0.012;  // ~3.7 s subtle pulse
}

// ── PULSES ────────────────────────────────────────────────────────────────
// A pulse is a signal travelling from one star to another along their
// connection line. We keep a small live pool and respawn pulses on a few
// random edges at a time, so most of the web stays dark.
const MAX_PULSES = Math.min(20, Math.max(5, Math.floor(EDGES.length / 27)));
const pulses = [];
function spawnPulse(){
  if(EDGES.length === 0) return;
  const e = EDGES[Math.floor(Math.random() * EDGES.length)];
  // 8% chance of a slow, brighter "thought" pulse
  const big = Math.random() < 0.08;
  pulses.push({
    a: e.a, b: e.b,
    t: 0,
    speed: big ? 0.45 + Math.random()*0.2 : 0.8 + Math.random()*0.6,
    bright: big ? 1.0 : 0.55 + Math.random() * 0.25,
    width:  big ? 1.6 : 0.9 + Math.random() * 0.4,
  });
}
for(let i = 0; i < Math.min(6, MAX_PULSES); i++) spawnPulse();

// ── INTERACTION STATE ─────────────────────────────────────────────────────
let dragging = false, moved = false, lastMouse = { x: 0, y: 0 };
let hovered = null, focused = null;

// ── DRAW ──────────────────────────────────────────────────────────────────
let time = 0;          // raw elapsed time (always advances) — for UI animation etc.
let renderTime = 0;    // advances only when the mind is not frozen — used for breath, spin, twinkle
let lastFrame = performance.now();

function draw(now){
  const dt = Math.min(0.05, (now - lastFrame) / 1000); // clamp delta
  lastFrame = now;
  time += dt;
  if(!app.frozen) renderTime += dt;

  // 1) clear to the cream ground
  ctx.fillStyle = '#F7F1E8';
  ctx.fillRect(0, 0, W, H);

  // 2) breathing — every star and centre scales radially from origin
  const breath = breathScale(renderTime);

  // 3) project every star once (and cache positions for pulses + picking)
  //    Each star's actual world position is:
  //      centre + rotate(offset * gravity, centre.axis, renderTime*spinSpeed)
  //    So changing gravity expands/contracts every cluster, and each
  //    constellation rotates on its own axis independently of the camera.
  const projStars = new Array(STARS.length);
  const grav = app.visual.gravity;
  for(let i = 0; i < STARS.length; i++){
    const s = STARS[i];
    // pull centre once
    const c = (s.ci != null) ? CENTRES[s.ci] : null;
    let bx, by, bz;
    if(c && typeof s.ox === 'number'){
      // rotate the local offset by the constellation's own angle
      const angle = (c.spinPhase || 0) + renderTime * (c.spinSpeed || 0) * app.visual.constellationSpin;
      const ax = c.ax, ay = c.ay, az = c.az;
      // Rodrigues' rotation: v_rot = v*cos + (k×v)*sin + k*(k·v)*(1-cos)
      const ox = s.ox * grav, oy = s.oy * grav, oz = s.oz * grav;
      const cos = Math.cos(angle), sin = Math.sin(angle);
      const kdot = ax * ox + ay * oy + az * oz;
      const kx = ay * oz - az * oy;
      const ky = az * ox - ax * oz;
      const kz = ax * oy - ay * ox;
      const rx = ox * cos + kx * sin + ax * kdot * (1 - cos);
      const ry = oy * cos + ky * sin + ay * kdot * (1 - cos);
      const rz = oz * cos + kz * sin + az * kdot * (1 - cos);
      bx = c.x + rx; by = c.y + ry; bz = c.z + rz;
    } else {
      bx = s.x; by = s.y; bz = s.z;
    }
    // micro per-star wobble — keeps the field alive without drifting it
    const wob = Math.sin(renderTime * (s.speed||1) + (s.phase||0)) * 1.2;
    const x = bx * breath + wob * 0.5;
    const y = by * breath + wob * 0.3;
    const z = bz * breath + wob * 0.4;
    projStars[i] = project(x, y, z);
    projStars[i].star = s;
  }

  // 4) GLOBAL NEBULA — one soft cloud around the entire mindmap.
  //    Drifts very slowly as if blown by cosmic wind. Made of a few stacked
  //    coloured wisps that translate and rotate at slightly different rates,
  //    so the motion is barely perceptible but always alive.
  {
    // mind centre is world (0,0,0); project it to screen for the nebula anchor
    const mc = project(0, 0, 0);
    const sphereR = 380;
    const baseR = sphereR * 1.55 * cam.scale;

    // Nebula colour mode: 'auto' uses the default 4-wisp palette; otherwise
    // every wisp uses (variants of) a single chosen hue for a unified mood.
    const NEBULA_PALETTES = {
      auto:   ['#CBCFAB','#DDC6A6','#AEB9BC','#C4A398'],
      blue:   ['#AEB9BC','#6F838C','#A9B4B8','#8E9CA3'],
      violet: ['#C4A398','#B98F84','#D2B6AC','#A07D72'],
      teal:   ['#CBCFAB','#A3A696','#B8C0A0','#8E9A78'],
      amber:  ['#E6D3A8','#D4A93E','#DDC6A6','#C9A76E'],
      rose:   ['#C4A398','#D8BFB5','#B99D84','#C9A99C'],
      mono:   ['#D2D2CA','#B9B9B0','#A5A79A','#C7C3B8'],
      custom: [app.visual.nebulaCustom, app.visual.nebulaCustom,
               app.visual.nebulaCustom, app.visual.nebulaCustom],
    };
    const cols = NEBULA_PALETTES[app.visual.nebulaColor] || NEBULA_PALETTES.auto;
    const wisps = [
      // [weight, speed, size factor, phase]
      [0.10, 0.013, 1.00, 0.0],
      [0.08, 0.009, 1.20, 2.1],
      [0.07, 0.011, 1.10, 4.0],
      [0.06, 0.007, 1.35, 1.2],
    ];
    const opacityMul = app.visual.nebulaOpacity * (app.connectMode ? 0.25 : 1);
    for(let i = 0; i < wisps.length; i++){
      const col = cols[i % cols.length];
      const [weight, speed, sz, ph] = wisps[i];
      const driftA = renderTime * speed + ph;
      // very small amplitude — barely perceptible cosmic wind
      const driftX = Math.cos(driftA) * baseR * 0.06
                   + Math.cos(driftA * 0.37) * baseR * 0.03;
      const driftY = Math.sin(driftA * 0.83) * baseR * 0.05
                   + Math.sin(driftA * 0.21 + 1.3) * baseR * 0.03;
      const wx = mc.sx + driftX;
      const wy = mc.sy + driftY;
      const wr = baseR * sz;
      const g = ctx.createRadialGradient(wx, wy, 0, wx, wy, wr);
      g.addColorStop(0,    col + '22');
      g.addColorStop(0.45, col + '10');
      g.addColorStop(0.8,  col + '06');
      g.addColorStop(1,    'transparent');
      ctx.fillStyle = g;
      ctx.globalAlpha = weight * 3.5 * opacityMul;
      ctx.beginPath(); ctx.arc(wx, wy, wr, 0, Math.PI * 2); ctx.fill();
    }
    ctx.globalAlpha = 1;
  }


  // 4b) Draw the constellation SYNAPSES — faint always-visible lines linking
  //     stars within the same cluster. They appear as a delicate filigree of
  //     "thought-threads" inside each constellation.
  ctx.lineCap = 'round';
  const filterOn = app.statusFilter && app.statusFilter !== 'all';
  const connectOn = !!app.connectMode;
  const searchOn = !!app.searchQuery;
  const tlAtSyn = app.timelapseAt;
  for(const syn of SYNAPSES){
    const pa = projStars[syn.a], pb = projStars[syn.b];
    if(!pa || !pb) continue;
    if(pa.depth < -cam.dist * 0.9 || pb.depth < -cam.dist * 0.9) continue;
    if(tlAtSyn != null){
      const da = STARS[syn.a].dateAdded, db = STARS[syn.b].dateAdded;
      if((da && da > tlAtSyn) || (db && db > tlAtSyn)) continue;
    }
    const avgPersp = (pa.persp + pb.persp) * 0.5;
    const shimmer = 0.5 + 0.5 * Math.sin(renderTime * 0.8 + (syn.a * 0.31 + syn.b * 0.19));
    let alpha = 0.34 * avgPersp * (0.65 + 0.35 * shimmer);
    if(connectOn){
      const okA = syn.a === app.connectMode.sourceIdx || app.connectMode.lit.has(syn.a);
      const okB = syn.b === app.connectMode.sourceIdx || app.connectMode.lit.has(syn.b);
      if(!(okA && okB)) alpha *= 0.04;
    } else {
      let bothOk = true;
      if(filterOn){
        const okA = peekStatus(STARS[syn.a]) === app.statusFilter;
        const okB = peekStatus(STARS[syn.b]) === app.statusFilter;
        if(!(okA && okB)) bothOk = false;
      }
      if(searchOn && bothOk){
        const okA = starMatchesSearch(STARS[syn.a], app.searchQuery);
        const okB = starMatchesSearch(STARS[syn.b], app.searchQuery);
        if(!(okA && okB)) bothOk = false;
      }
      if(!bothOk) alpha *= 0.10;
    }
    ctx.strokeStyle = STARS[syn.a].color;
    ctx.globalAlpha = alpha;
    ctx.lineWidth = Math.max(0.5, 0.9 * avgPersp);
    ctx.beginPath();
    ctx.moveTo(pa.sx, pa.sy);
    ctx.lineTo(pb.sx, pb.sy);
    ctx.stroke();
  }
  ctx.globalAlpha = 1;

  // 4c) CONNECTION-VIEW lines — when the user has asked to see one star's
  //     connections, draw a curved bright line from the source to each
  //     connected star. Drawn above the synapse web but below the stars.
  if(app.connectMode){
    const sIdx = app.connectMode.sourceIdx;
    const ps = projStars[sIdx];
    if(ps){
      ctx.lineCap = 'round';
      for(const j of app.connectMode.lit){
        if(j === sIdx) continue;
        const pj = projStars[j];
        if(!pj) continue;
        if(ps.depth < -cam.dist * 0.9 && pj.depth < -cam.dist * 0.9) continue;
        // Bezier control pulled toward the screen centre — same trick as pulses
        const cx2 = (ps.sx + pj.sx) * 0.5 + ((ps.sx + pj.sx) * 0.5 - W * 0.5) * -0.14;
        const cy2 = (ps.sy + pj.sy) * 0.5 + ((ps.sy + pj.sy) * 0.5 - H * 0.5) * -0.14;
        // Draw the curve in target-star's colour, fading toward the source
        const col = STARS[j].color || '#6F838C';
        ctx.strokeStyle = col;
        ctx.globalAlpha = 0.62;
        const avgPersp = (ps.persp + pj.persp) * 0.5;
        ctx.lineWidth = Math.max(0.9, 1.4 * avgPersp);
        ctx.beginPath();
        ctx.moveTo(ps.sx, ps.sy);
        ctx.quadraticCurveTo(cx2, cy2, pj.sx, pj.sy);
        ctx.stroke();
      }
      ctx.globalAlpha = 1;
    }
  }

  // 5) draw stars (back-to-front for proper layering)
  const order = projStars.map((_, i) => i).sort((a, b) => projStars[b].depth - projStars[a].depth);
  const tlAt = app.timelapseAt;
  for(const idx of order){
    const p = projStars[idx];
    const s = p.star;
    if(p.depth < -cam.dist * 0.9) continue;
    // Time-lapse: skip stars added after the current cutoff
    if(tlAt != null && s.dateAdded && s.dateAdded > tlAt) continue;
    const twinkle = (Math.sin(renderTime * (s.speed||1) * 2.0 + (s.phase||0)) + 1) * 0.5;
    const isH = (s === hovered), isF = (s === focused);
    // Look up status (read-only) — used for ring + filter dimming.
    const status = peekStatus(s);
    // Connection-view takes priority: when active, only the source + its
    // connected stars stay bright; everything else dims to near-black.
    let dim, isLit = false, isSource = false;
    if(app.connectMode){
      isSource = (idx === app.connectMode.sourceIdx);
      isLit    = isSource || app.connectMode.lit.has(idx);
      dim = isLit ? 1.0 : 0.05;
    } else {
      // Combine status filter + search query — must satisfy BOTH to stay bright
      const filterActive = app.statusFilter && app.statusFilter !== 'all';
      const statusOk = !filterActive || status === app.statusFilter;
      const searchOk = !app.searchQuery || starMatchesSearch(s, app.searchQuery);
      dim = (statusOk && searchOk) ? 1.0 : 0.10;
    }
    // In connection-view, lit stars get a bigger base radius and brighter aura.
    const litBoost = (isLit && !isSource) ? 1.35 : (isSource ? 1.6 : 1.0);
    const baseR = (s.size || 1) * (isH ? 4.62 : (isF ? 3.85 : 2.64)) * p.persp * cam.scale * 0.9 * litBoost;
    const r = Math.max(0.66, baseR * (0.85 + 0.25 * twinkle));

    // outer aura — alpha bumped ~10% in each state
    const auraR = r * (isH || isLit ? 7 : 5);
    const aura = ctx.createRadialGradient(p.sx, p.sy, 0, p.sx, p.sy, auraR);
    const auraAlpha = isH ? '55' : (isF || isSource ? '4a' : (isLit ? '3a' : '1e'));
    aura.addColorStop(0,    s.color + auraAlpha);
    aura.addColorStop(0.3,  s.color + '12');
    aura.addColorStop(1,    'transparent');
    ctx.globalAlpha = dim;
    ctx.fillStyle = aura;
    ctx.beginPath(); ctx.arc(p.sx, p.sy, auraR, 0, Math.PI * 2); ctx.fill();

    // bright core
    ctx.fillStyle = s.color;
    ctx.beginPath(); ctx.arc(p.sx, p.sy, Math.max(2.2, r * 1.15), 0, Math.PI * 2); ctx.fill();
    ctx.globalAlpha = 1;

    // STATUS RING — subtle marker for non-default statuses
    const styling = STATUS_STYLES[status];
    if(styling){
      const ringR = r * 2.4 + 2;
      ctx.save();
      ctx.strokeStyle = styling.color;
      // ring alpha follows the dim multiplier so filtered-out stars stay calm
      ctx.globalAlpha = 0.85 * dim;
      ctx.lineWidth = Math.max(0.8, r * 0.32);
      if(styling.style === 'dashed'){
        ctx.setLineDash([Math.max(1.5, r * 0.6), Math.max(1.5, r * 0.6)]);
      }
      ctx.beginPath(); ctx.arc(p.sx, p.sy, ringR, 0, Math.PI * 2); ctx.stroke();
      ctx.setLineDash([]);
      if(styling.style === 'solid-dot'){
        // a small inner dot in the ring colour — the "finished" tick
        ctx.fillStyle = styling.color;
        ctx.globalAlpha = 0.95 * dim;
        ctx.beginPath(); ctx.arc(p.sx, p.sy, Math.max(1, r * 0.4), 0, Math.PI * 2); ctx.fill();
      }
      ctx.restore();
    }

    // focused ring
    if(isF){
      ctx.strokeStyle = '#2F3B4B';
      ctx.globalAlpha = 0.9;
      ctx.lineWidth = 1.5;
      ctx.beginPath(); ctx.arc(p.sx, p.sy, r * 3 + 4, 0, Math.PI * 2); ctx.stroke();
      ctx.globalAlpha = 1;
    }
  }

  // 5b) CONSTELLATION LABELS — italic name floating above each cluster.
  // Visible only when zoomed out (so individual stars aren't cluttered) and
  // hidden in connect-mode (a different lens, different signal). The label
  // alpha smoothly fades between zoom thresholds for a graceful appearance.
  if(!app.connectMode && app.visual.showLabels){
    const zoomLerp = 1 - Math.max(0, Math.min(1, (cam.scale - 0.85) / 0.85));
    if(zoomLerp > 0.02){
      const breath = breathScale(renderTime);
      // In time-lapse, count how many stars are currently visible per centre
      // so we can hide labels for constellations that don't exist yet.
      let visibleByCi = null;
      if(app.timelapseAt != null){
        visibleByCi = new Array(CENTRES.length).fill(0);
        for(const s of STARS){
          if(s.ci == null) continue;
          if(!s.dateAdded || s.dateAdded <= app.timelapseAt) visibleByCi[s.ci]++;
        }
      }
      ctx.save();
      ctx.font = "italic 14px 'Cormorant Garamond', serif";
      ctx.textAlign = 'center';
      ctx.textBaseline = 'middle';
      for(let i = 0; i < CENTRES.length; i++){
        const c = CENTRES[i];
        const cp = project(c.x * breath, c.y * breath, c.z * breath);
        if(cp.depth < -cam.dist * 0.9) continue;
        if(!c.count) continue;
        if(visibleByCi && !visibleByCi[i]) continue;
        const a = 0.62 * zoomLerp * Math.min(1, cp.persp * 1.4);
        if(a < 0.04) continue;
        ctx.globalAlpha = a * 0.9;
        ctx.strokeStyle = '#F7F1E8';
        ctx.lineWidth = 4;
        ctx.strokeText(c.subject, cp.sx, cp.sy);
        ctx.globalAlpha = Math.min(1, a * 1.3);
        ctx.fillStyle = '#2F3B4B';
        ctx.fillText(c.subject, cp.sx, cp.sy);
      }
      ctx.restore();
    }
  }

  // 6) draw pulses — short bright signals travelling along their edge
  const pulseDt = app.frozen ? 0 : dt;
  const tlAtPulse = app.timelapseAt;
  for(let i = pulses.length - 1; i >= 0; i--){
    const pu = pulses[i];
    pu.t += pulseDt * pu.speed;
    if(pu.t >= 1){
      pulses.splice(i, 1);
      continue;
    }
    const pa = projStars[pu.a], pb = projStars[pu.b];
    if(!pa || !pb) continue;
    if(pa.depth < -cam.dist*0.9 && pb.depth < -cam.dist*0.9) continue;
    // In time-lapse, suppress pulses whose endpoints don't exist yet
    if(tlAtPulse != null){
      const da = STARS[pu.a].dateAdded, db = STARS[pu.b].dateAdded;
      if((da && da > tlAtPulse) || (db && db > tlAtPulse)) continue;
    }

    // signal "head" leads, "tail" trails behind by a small fraction
    const head = pu.t;
    const tail = Math.max(0, pu.t - 0.18);
    // bezier control point: pulled toward the screen centre for a graceful arc
    const cx = (pa.sx + pb.sx) * 0.5 + ((pa.sx + pb.sx) * 0.5 - W * 0.5) * -0.18;
    const cy = (pa.sy + pb.sy) * 0.5 + ((pa.sy + pb.sy) * 0.5 - H * 0.5) * -0.18;

    // draw a short bright segment from tail->head along the bezier
    const STEPS = 14;
    ctx.lineCap = 'round';
    for(let k = 0; k < STEPS; k++){
      const t0 = tail + (head - tail) * (k     / STEPS);
      const t1 = tail + (head - tail) * ((k+1) / STEPS);
      const omt0 = 1 - t0, omt1 = 1 - t1;
      const x0 = omt0*omt0*pa.sx + 2*omt0*t0*cx + t0*t0*pb.sx;
      const y0 = omt0*omt0*pa.sy + 2*omt0*t0*cy + t0*t0*pb.sy;
      const x1 = omt1*omt1*pa.sx + 2*omt1*t1*cx + t1*t1*pb.sx;
      const y1 = omt1*omt1*pa.sy + 2*omt1*t1*cy + t1*t1*pb.sy;
      // brightness fades from tail to head
      const a = (k / STEPS) * pu.bright;
      // colour: blend the two endpoints' colours
      const c = STARS[pu.a].color;
      ctx.strokeStyle = c;
      ctx.globalAlpha = a;
      ctx.lineWidth = pu.width;
      ctx.beginPath();
      ctx.moveTo(x0, y0); ctx.lineTo(x1, y1);
      ctx.stroke();
    }
    // bright leading dot at the head
    const omh = 1 - head;
    const hx = omh*omh*pa.sx + 2*omh*head*cx + head*head*pb.sx;
    const hy = omh*omh*pa.sy + 2*omh*head*cy + head*head*pb.sy;
    const headColor = STARS[pu.a].color;
    const dotR = pu.width * 1.6;
    const dotGl = ctx.createRadialGradient(hx, hy, 0, hx, hy, dotR * 5);
    dotGl.addColorStop(0,    headColor + 'ff');
    dotGl.addColorStop(0.5,  headColor + '40');
    dotGl.addColorStop(1,    'transparent');
    ctx.fillStyle = dotGl;
    ctx.globalAlpha = pu.bright;
    ctx.beginPath(); ctx.arc(hx, hy, dotR * 5, 0, Math.PI*2); ctx.fill();
    ctx.fillStyle = headColor;
    ctx.globalAlpha = pu.bright;
    ctx.beginPath(); ctx.arc(hx, hy, dotR, 0, Math.PI*2); ctx.fill();
    ctx.globalAlpha = 1;
  }

  // 7) keep the pulse pool replenished — but stagger so the web stays sparse
  if(pulses.length < MAX_PULSES && Math.random() < 0.044){
    spawnPulse();
  }

  // 8) hovered/focused star label
  if(hovered){
    const i = STARS.indexOf(hovered);
    if(i >= 0){
      const p = projStars[i];
      ctx.font = "500 13px 'Figtree', sans-serif";
      ctx.textAlign = 'left';
      ctx.textBaseline = 'middle';
      ctx.fillStyle = '#2F3B4B';
      ctx.globalAlpha = 0.95;
      ctx.fillText(hovered.title, p.sx + 14, p.sy);
      ctx.globalAlpha = 1;
    }
  }

  requestAnimationFrame(draw);
}
requestAnimationFrame(draw);

// ── PICKING ───────────────────────────────────────────────────────────────
function pickStar(sx, sy){
  // sx/sy in canvas (device-pixel) coords. Must use the SAME live position
  // math as the draw loop, or taps won't land on rotating/scaled stars.
  let best = null, bestD = 24 * DPR;
  const breath = breathScale(renderTime);
  const grav = app.visual.gravity;
  for(const s of STARS){
    const c = (s.ci != null) ? CENTRES[s.ci] : null;
    let bx, by, bz;
    if(c && typeof s.ox === 'number'){
      const angle = (c.spinPhase || 0) + renderTime * (c.spinSpeed || 0) * app.visual.constellationSpin;
      const ax = c.ax, ay = c.ay, az = c.az;
      const ox = s.ox * grav, oy = s.oy * grav, oz = s.oz * grav;
      const cos = Math.cos(angle), sin = Math.sin(angle);
      const kdot = ax * ox + ay * oy + az * oz;
      const kx = ay * oz - az * oy;
      const ky = az * ox - ax * oz;
      const kz = ax * oy - ay * ox;
      const rx = ox * cos + kx * sin + ax * kdot * (1 - cos);
      const ry = oy * cos + ky * sin + ay * kdot * (1 - cos);
      const rz = oz * cos + kz * sin + az * kdot * (1 - cos);
      bx = c.x + rx; by = c.y + ry; bz = c.z + rz;
    } else {
      bx = s.x; by = s.y; bz = s.z;
    }
    const p = project(bx * breath, by * breath, bz * breath);
    if(p.depth < -cam.dist * 0.9) continue;
    const d = Math.hypot(p.sx - sx, p.sy - sy);
    if(d < bestD){ bestD = d; best = s; }
  }
  return best;
}

// bookData is the read/write accessor (peekStatus + makeBookKey + STATUS_STYLES
// are declared near the top of this script so the draw loop can read status
// without hitting a TDZ).
function bookData(s){
  const k = makeBookKey(s);
  if(!app.bookData[k]) app.bookData[k] = { notes: '', rating: 0, status: 'unread', description: '' };
  return app.bookData[k];
}

// ── COVER ART (OpenLibrary) ─────────────────────────────────────────────
// Lookup table: book key -> Promise<url|null>. Cached in memory for the
// session so we don't re-query the API for the same book on every open.
// OpenLibrary's Search API is free and key-less. We query by title +
// author, take the first hit's cover_i, then build the covers URL.
const coverCache = {};
async function fetchCover(s){
  const k = makeBookKey(s);
  if(k in coverCache) return coverCache[k];
  const title = (s.title || '').trim();
  if(!title){ coverCache[k] = null; return null; }
  const author = (s.author && s.author !== 'Unknown') ? s.author : '';
  const params = new URLSearchParams();
  params.set('title', title);
  if(author) params.set('author', author);
  params.set('limit', '1');
  // Cache the promise itself so concurrent calls share one fetch
  const p = (async () => {
    try {
      const url = 'https://openlibrary.org/search.json?' + params.toString();
      const res = await fetch(url);
      if(!res.ok) return null;
      const data = await res.json();
      const doc = (data && data.docs && data.docs[0]) || null;
      if(!doc) return null;
      if(doc.cover_i){
        return 'https://covers.openlibrary.org/b/id/' + doc.cover_i + '-L.jpg';
      }
      if(doc.cover_edition_key){
        return 'https://covers.openlibrary.org/b/olid/' + doc.cover_edition_key + '-L.jpg';
      }
      // ISBN fallback if present
      if(Array.isArray(doc.isbn) && doc.isbn.length){
        return 'https://covers.openlibrary.org/b/isbn/' + doc.isbn[0] + '-L.jpg';
      }
      return null;
    } catch(e){ return null; }
  })();
  coverCache[k] = p;
  // Resolve the slot to the actual url|null when done (so future calls don't await again)
  p.then(v => { coverCache[k] = v; });
  return p;
}

// Cover backdrop for the small tooltip. The cover fades in if the fetch
// resolves before the tooltip changes target. Each call carries a token so
// late-arriving fetches don't paint into the wrong tooltip.
let _ttCoverToken = 0;
function loadTooltipCover(s){
  const el = document.getElementById('tt-cover');
  if(!el) return;
  // Reset to invisible immediately so the previous book's cover doesn't
  // linger while the new fetch is in flight.
  el.classList.remove('loaded');
  el.style.backgroundImage = 'none';
  if(!s) return;
  const myToken = ++_ttCoverToken;
  Promise.resolve(fetchCover(s)).then(url => {
    if(myToken !== _ttCoverToken) return;       // a newer tooltip target won
    if(!url) return;
    // Preload so we don't flash a partial image
    const img = new Image();
    img.referrerPolicy = 'no-referrer';
    img.onload = () => {
      if(myToken !== _ttCoverToken) return;
      el.style.backgroundImage = 'url("' + url + '")';
      requestAnimationFrame(() => { el.classList.add('loaded'); });
    };
    img.src = url;
  });
}
function clearTooltipCover(){
  _ttCoverToken++;     // invalidate any pending fetch
  const el = document.getElementById('tt-cover');
  if(!el) return;
  el.classList.remove('loaded');
  el.style.backgroundImage = 'none';
}

function setTooltip(s, clientX, clientY){
  const tt = document.getElementById('tooltip');
  if(!s){ tt.classList.remove('visible'); clearTooltipCover(); return; }
  // when a tooltip is already pinned, don't repaint it from hovers
  if(tt.classList.contains('pinned')) return;
  tt.classList.add('visible');
  tt.classList.remove('pinned');
  tt.style.left = (clientX + 16) + 'px';
  tt.style.top  = (clientY - 10) + 'px';
  const c = s.color || '#6F838C';
  document.getElementById('tt-accent').style.background = c;
  document.getElementById('tt-kind').textContent = (s.subject || 'unsorted');
  document.getElementById('tt-title').textContent = s.title;
  document.getElementById('tt-author').textContent = s.author + (s.year ? ' · ' + s.year : '');
  const tags = document.getElementById('tt-tags'); tags.innerHTML = '';
  const status = peekStatus(s);
  if(status && status !== 'unread'){
    const sc = (STATUS_STYLES[status] || {}).color || '#6F838C';
    tags.innerHTML += `<span class="tt-tag" style="color:${sc};border-color:${sc}66">● ${status}</span>`;
  }
  if(s.genre) tags.innerHTML += `<span class="tt-tag genre-tag" style="color:${c};border-color:${c}55">${s.genre}</span>`;
  (s.subjects || []).forEach(x => { tags.innerHTML += `<span class="tt-tag">${x}</span>`; });
  document.getElementById('tt-actions').classList.add('hidden');
  loadTooltipCover(s);
}

// Pin the tooltip on a focused star: freeze the mind, show action buttons,
// position the tooltip near the star's projected screen position, and lock it
// open until the user dismisses.
function pinTooltip(s){
  if(!s) { unpinTooltip(); return; }
  app.frozen = true;
  focused = s;
  const tt = document.getElementById('tooltip');
  // Always exit edit mode when re-pinning (covers switching focus to a different star)
  tt.classList.remove('editing');
  // Position near the star (use latest projected position). We compute it
  // here so the tooltip lands where the star actually is on screen.
  let cx = innerWidth / 2, cy = innerHeight / 2;
  const idx = STARS.indexOf(s);
  if(idx >= 0){
    // Re-project this star with the held renderTime so its on-screen point
    // matches what the user sees right now.
    const breath = breathScale(renderTime);
    const grav = app.visual.gravity;
    const c = (s.ci != null) ? CENTRES[s.ci] : null;
    let bx, by, bz;
    if(c && typeof s.ox === 'number'){
      const angle = (c.spinPhase||0) + renderTime * (c.spinSpeed||0) * app.visual.constellationSpin;
      const ax = c.ax, ay = c.ay, az = c.az;
      const ox = s.ox * grav, oy = s.oy * grav, oz = s.oz * grav;
      const cos = Math.cos(angle), sin = Math.sin(angle);
      const kdot = ax*ox + ay*oy + az*oz;
      const kx = ay*oz - az*oy, ky = az*ox - ax*oz, kz = ax*oy - ay*ox;
      const rx = ox*cos + kx*sin + ax*kdot*(1-cos);
      const ry = oy*cos + ky*sin + ay*kdot*(1-cos);
      const rz = oz*cos + kz*sin + az*kdot*(1-cos);
      bx = c.x + rx; by = c.y + ry; bz = c.z + rz;
    } else { bx = s.x; by = s.y; bz = s.z; }
    const p = project(bx*breath, by*breath, bz*breath);
    cx = p.sx / DPR; cy = p.sy / DPR;
  }
  tt.classList.add('visible','pinned');
  // Position the tooltip near the star, clamped to viewport
  // We use the existing setTooltip body to fill fields, then re-position.
  const c = s.color || '#6F838C';
  document.getElementById('tt-accent').style.background = c;
  document.getElementById('tt-kind').textContent = (s.subject || 'unsorted');
  document.getElementById('tt-title').textContent = s.title;
  document.getElementById('tt-author').textContent = s.author + (s.year ? ' · ' + s.year : '');
  const tags = document.getElementById('tt-tags'); tags.innerHTML = '';
  const status = peekStatus(s);
  if(status && status !== 'unread'){
    const sc = (STATUS_STYLES[status] || {}).color || '#6F838C';
    tags.innerHTML += `<span class="tt-tag" style="color:${sc};border-color:${sc}66">● ${status}</span>`;
  }
  if(s.genre) tags.innerHTML += `<span class="tt-tag genre-tag" style="color:${c};border-color:${c}55">${s.genre}</span>`;
  (s.subjects || []).forEach(x => { tags.innerHTML += `<span class="tt-tag">${x}</span>`; });
  document.getElementById('tt-actions').classList.remove('hidden');
  loadTooltipCover(s);
  // After paint, measure and clamp
  requestAnimationFrame(() => {
    const rect = tt.getBoundingClientRect();
    const PAD = 12;
    let left = cx + 18, top = cy - rect.height / 2;
    if(left + rect.width + PAD > innerWidth) left = cx - rect.width - 18;
    if(left < PAD) left = PAD;
    if(top < PAD) top = PAD;
    if(top + rect.height + PAD > innerHeight) top = innerHeight - rect.height - PAD;
    tt.style.left = left + 'px';
    tt.style.top  = top + 'px';
  });
}

function unpinTooltip(){
  app.frozen = false;
  focused = null;
  const tt = document.getElementById('tooltip');
  tt.classList.remove('pinned','visible','editing');
  document.getElementById('tt-actions').classList.add('hidden');
  clearTooltipCover();
}

// Tooltip action buttons
document.getElementById('tt-close').addEventListener('click', e => { e.stopPropagation(); unpinTooltip(); });
document.getElementById('tt-dismiss').addEventListener('click', e => { e.stopPropagation(); unpinTooltip(); });
document.getElementById('tt-expand').addEventListener('click', e => {
  e.stopPropagation();
  const target = focused;
  if(!target) return;
  // Hide the small tooltip — the expanded modal takes over.
  // Keep the mind frozen while the modal is open so the user can study
  // the book in peace; closing the modal will unfreeze.
  const tt = document.getElementById('tooltip');
  tt.classList.remove('visible', 'pinned');
  document.getElementById('tt-actions').classList.add('hidden');
  clearTooltipCover();
  openBookDetail(target);
});
document.getElementById('tt-connect').addEventListener('click', e => {
  e.stopPropagation();
  if(focused) enterConnectMode(focused);
});
// Quick edit (title + author only) — opens inline inputs inside the pinned tooltip.
document.getElementById('tt-edit').addEventListener('click', e => {
  e.stopPropagation();
  if(focused) enterTooltipEditMode(focused);
});
document.getElementById('tt-save').addEventListener('click', e => {
  e.stopPropagation();
  exitTooltipEditMode(true);
});
document.getElementById('tt-cancel').addEventListener('click', e => {
  e.stopPropagation();
  exitTooltipEditMode(false);
});
// Input keypress handlers: Enter commits, Escape cancels, all other keys
// stop propagation so they don't trigger canvas / app shortcuts.
['tt-title-input','tt-author-input'].forEach(id => {
  const el = document.getElementById(id);
  el.addEventListener('keydown', e => {
    if(e.key === 'Enter'){ e.preventDefault(); exitTooltipEditMode(true); }
    else if(e.key === 'Escape'){ e.preventDefault(); exitTooltipEditMode(false); }
    e.stopPropagation();
  });
});

// ── TOOLTIP QUICK-EDIT HELPERS ──────────────────────────────────────────
// Edit mode is intentionally narrow: just title and author. Subjects, genre,
// year, etc. live in the Expand panel since changing subject has structural
// consequences (constellation membership).
function enterTooltipEditMode(s){
  if(!s) return;
  const tt = document.getElementById('tooltip');
  document.getElementById('tt-title-input').value = s.title || '';
  document.getElementById('tt-author-input').value = (s.author && s.author !== 'Unknown') ? s.author : '';
  tt.classList.add('editing');
  // Re-position after layout shift (inputs may make the tooltip taller)
  requestAnimationFrame(() => {
    document.getElementById('tt-title-input').focus();
    document.getElementById('tt-title-input').select();
  });
}
function exitTooltipEditMode(commit){
  const tt = document.getElementById('tooltip');
  if(commit){
    const s = focused;
    if(!s){ tt.classList.remove('editing'); return; }
    const newTitle = document.getElementById('tt-title-input').value.trim();
    const newAuthor = document.getElementById('tt-author-input').value.trim() || 'Unknown';
    if(!newTitle){ toast('Title cannot be empty'); return; }
    const oldKey = makeBookKey(s);
    s.title = newTitle;
    s.author = newAuthor;
    const newKey = makeBookKey(s);
    // Migrate any saved bookData (notes / rating / status) to the new key
    if(oldKey !== newKey){
      if(app.bookData[oldKey]){
        app.bookData[newKey] = app.bookData[oldKey];
        delete app.bookData[oldKey];
      }
      // Invalidate cover cache so the next lookup uses the corrected title
      delete coverCache[oldKey];
      delete coverCache[newKey];
    }
    // Refresh the static display lines
    const c = s.color || '#6F838C';
    document.getElementById('tt-title').textContent = s.title;
    document.getElementById('tt-author').textContent = s.author + (s.year ? ' · ' + s.year : '');
    // Re-load cover (title may have changed)
    loadTooltipCover(s);
    saveState();
    toast('Updated');
  }
  tt.classList.remove('editing');
}

// Prevent clicks inside the tooltip from bubbling out and unfocusing
document.getElementById('tooltip').addEventListener('mousedown', e => e.stopPropagation());
document.getElementById('tooltip').addEventListener('touchstart', e => e.stopPropagation(), { passive: true });

document.getElementById('connect-hint').addEventListener('click', e => {
  e.stopPropagation();
  exitConnectMode();
});

// ── CONNECTION-VIEW ─────────────────────────────────────────────────────
// "Show connections" picks every book sharing an author, genre, or any
// subject with the source star, dims everything else to near-black, draws
// curves from the source to each connection, and recenters the camera on
// the source star.
function computeConnections(sourceIdx){
  const lit = new Set();
  const src = STARS[sourceIdx];
  if(!src) return lit;
  const srcSubjects = new Set((src.subjects || []).map(t => String(t).toLowerCase()));
  const srcGenre  = (src.genre  || '').toLowerCase();
  const srcAuthor = (src.author || '').toLowerCase();
  for(let i = 0; i < STARS.length; i++){
    if(i === sourceIdx) continue;
    const t = STARS[i];
    const tSubjects = (t.subjects || []).map(x => String(x).toLowerCase());
    if(tSubjects.some(x => srcSubjects.has(x))){ lit.add(i); continue; }
    if(srcGenre  && (t.genre  || '').toLowerCase() === srcGenre){  lit.add(i); continue; }
    if(srcAuthor && (t.author || '').toLowerCase() === srcAuthor){ lit.add(i); continue; }
  }
  return lit;
}

function enterConnectMode(star){
  const idx = STARS.indexOf(star);
  if(idx < 0) return;
  const lit = computeConnections(idx);
  app.connectMode = { sourceIdx: idx, lit };
  // Hide the small tooltip — the cosmos becomes the answer.
  const tt = document.getElementById('tooltip');
  tt.classList.remove('visible', 'pinned');
  document.getElementById('tt-actions').classList.add('hidden');
  clearTooltipCover();
  // Show the exit hint in the HUD
  document.getElementById('connect-hint').classList.add('visible');
  document.getElementById('connect-count').textContent = lit.size;
  // Recenter the camera on the source star.
  // We use the star's CURRENT live position (after gravity + rotation), not
  // its stored static x/y/z, so the camera lands on what the user actually sees.
  const live = liveStarPos(star);
  // Solve for camera angles that put `live` at screen centre.
  const targetRotY = Math.atan2(live.x, live.z);
  const targetRotX = Math.atan2(live.y, Math.hypot(live.x, live.z));
  animateCameraTo(targetRotY, targetRotX, 700);
  // Keep the mind frozen so connections sit still while the user reads them.
  app.frozen = true;
}

function exitConnectMode(){
  if(!app.connectMode) return;
  app.connectMode = null;
  app.frozen = false;
  document.getElementById('connect-hint').classList.remove('visible');
}

// Compute a star's live world position (with breath + gravity + constellation rot)
function liveStarPos(s){
  const breath = breathScale(renderTime);
  const grav = app.visual.gravity;
  const c = (s.ci != null) ? CENTRES[s.ci] : null;
  let bx, by, bz;
  if(c && typeof s.ox === 'number'){
    const angle = (c.spinPhase||0) + renderTime * (c.spinSpeed||0) * app.visual.constellationSpin;
    const ax = c.ax, ay = c.ay, az = c.az;
    const ox = s.ox * grav, oy = s.oy * grav, oz = s.oz * grav;
    const cos = Math.cos(angle), sin = Math.sin(angle);
    const kdot = ax*ox + ay*oy + az*oz;
    const kx = ay*oz - az*oy, ky = az*ox - ax*oz, kz = ax*oy - ay*ox;
    const rx = ox*cos + kx*sin + ax*kdot*(1-cos);
    const ry = oy*cos + ky*sin + ay*kdot*(1-cos);
    const rz = oz*cos + kz*sin + az*kdot*(1-cos);
    bx = c.x + rx; by = c.y + ry; bz = c.z + rz;
  } else { bx = s.x; by = s.y; bz = s.z; }
  return { x: bx * breath, y: by * breath, z: bz * breath };
}

// Camera tween — chooses the shortest angular path so the spin doesn't unwind.
let _camTween = null;
function animateCameraTo(targetY, targetX, durationMs){
  // Wrap rotY delta to (-π, π] for shortest path
  let dy = targetY - cam.rotY;
  while(dy >  Math.PI) dy -= 2*Math.PI;
  while(dy < -Math.PI) dy += 2*Math.PI;
  const finalY = cam.rotY + dy;
  const startY = cam.rotY, startX = cam.rotX;
  const start  = performance.now();
  _camTween = { start, durationMs, startY, startX, finalY, finalX: targetX };
}
function tickCamTween(now){
  if(!_camTween) return;
  const t = Math.min(1, (now - _camTween.start) / _camTween.durationMs);
  // ease-in-out cubic
  const e = t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2;
  cam.rotY = _camTween.startY + (_camTween.finalY - _camTween.startY) * e;
  cam.rotX = _camTween.startX + (_camTween.finalX - _camTween.startX) * e;
  if(t >= 1) _camTween = null;
}
// Hook into the auto-rotate side-RAF
(function camTweenLoop(){
  tickCamTween(performance.now());
  requestAnimationFrame(camTweenLoop);
})();

// ── MOUSE ─────────────────────────────────────────────────────────────────
canvas.addEventListener('mousedown', e => {
  dragging = true; moved = false;
  lastMouse = { x: e.clientX, y: e.clientY };
});
canvas.addEventListener('mousemove', e => {
  if(dragging){
    const dx = e.clientX - lastMouse.x, dy = e.clientY - lastMouse.y;
    if(Math.abs(dx) + Math.abs(dy) > 2) moved = true;
    // Block user rotation ONLY when a pinned tooltip is anchored to a star
    // (we don't want the star sliding out from under the tooltip). In
    // connect-mode the tooltip is hidden, so the user is free to orbit.
    const tooltipPinned = document.getElementById('tooltip').classList.contains('pinned');
    if(!tooltipPinned){
      cam.rotY += dx * 0.006;
      cam.rotX = Math.max(-Math.PI/2.05, Math.min(Math.PI/2.05, cam.rotX + dy * 0.006));
    }
    lastMouse = { x: e.clientX, y: e.clientY };
  }
  // Only update hover tooltip when not pinned (pinned tooltip is sticky)
  if(!document.getElementById('tooltip').classList.contains('pinned')){
    const s = pickStar(e.clientX * DPR, e.clientY * DPR);
    hovered = s;
    canvas.style.cursor = s ? 'pointer' : (dragging ? 'grabbing' : 'grab');
    setTooltip(s, e.clientX, e.clientY);
  }
});
canvas.addEventListener('mouseup', e => {
  dragging = false;
  if(!moved){
    const s = pickStar(e.clientX * DPR, e.clientY * DPR);
    if(s){
      if(app.connectMode){
        const sIdx = STARS.indexOf(s);
        const isLit = sIdx === app.connectMode.sourceIdx || app.connectMode.lit.has(sIdx);
        if(isLit && sIdx !== app.connectMode.sourceIdx){
          // Switch to that star's connections — keep frozen state continuous
          enterConnectMode(s);
        }
        // tapping the source again or a dimmed star does nothing
        return;
      }
      // Tap a star → pin tooltip and freeze the mind (or unpin if same star)
      if(focused === s) unpinTooltip();
      else pinTooltip(s);
    } else {
      // Tap empty space → exit any active mode
      if(app.connectMode) exitConnectMode();
      else if(focused) unpinTooltip();
    }
  }
});
canvas.addEventListener('mouseleave', () => {
  dragging = false;
  if(!document.getElementById('tooltip').classList.contains('pinned')){
    hovered = null; setTooltip(null);
  }
});

canvas.addEventListener('wheel', e => {
  e.preventDefault();
  const f = e.deltaY > 0 ? 0.92 : 1.08;
  cam.scale = Math.max(0.25, Math.min(5, cam.scale * f));
}, { passive: false });

// ── TOUCH ─────────────────────────────────────────────────────────────────
let touchMode = null, pinchStart = 0, pinchScaleStart = 1, tStart = { x: 0, y: 0 }, tMoved = false;
canvas.addEventListener('touchstart', e => {
  if(e.touches.length === 1){
    touchMode = 'rotate'; tMoved = false;
    lastMouse = { x: e.touches[0].clientX, y: e.touches[0].clientY };
    tStart = { x: e.touches[0].clientX, y: e.touches[0].clientY };
  } else if(e.touches.length === 2){
    touchMode = 'pinch';
    const dx = e.touches[0].clientX - e.touches[1].clientX;
    const dy = e.touches[0].clientY - e.touches[1].clientY;
    pinchStart = Math.hypot(dx, dy);
    pinchScaleStart = cam.scale;
  }
}, { passive: false });
canvas.addEventListener('touchmove', e => {
  e.preventDefault();
  if(touchMode === 'rotate' && e.touches.length === 1){
    const dx = e.touches[0].clientX - lastMouse.x;
    const dy = e.touches[0].clientY - lastMouse.y;
    if(Math.abs(e.touches[0].clientX - tStart.x) + Math.abs(e.touches[0].clientY - tStart.y) > 4) tMoved = true;
    const tooltipPinned = document.getElementById('tooltip').classList.contains('pinned');
    if(!tooltipPinned){
      cam.rotY += dx * 0.006;
      cam.rotX = Math.max(-Math.PI/2.05, Math.min(Math.PI/2.05, cam.rotX + dy * 0.006));
    }
    lastMouse = { x: e.touches[0].clientX, y: e.touches[0].clientY };
  } else if(touchMode === 'pinch' && e.touches.length === 2){
    const dx = e.touches[0].clientX - e.touches[1].clientX;
    const dy = e.touches[0].clientY - e.touches[1].clientY;
    const d = Math.hypot(dx, dy);
    cam.scale = Math.max(0.25, Math.min(5, pinchScaleStart * (d / pinchStart)));
  }
}, { passive: false });
canvas.addEventListener('touchend', e => {
  if(touchMode === 'rotate' && !tMoved){
    const s = pickStar(tStart.x * DPR, tStart.y * DPR);
    if(s){
      if(app.connectMode){
        const sIdx = STARS.indexOf(s);
        const isLit = sIdx === app.connectMode.sourceIdx || app.connectMode.lit.has(sIdx);
        if(isLit && sIdx !== app.connectMode.sourceIdx){
          enterConnectMode(s);
        }
        // else: ignore taps on dimmed stars or the source itself
      } else if(focused === s){
        unpinTooltip();
      } else {
        pinTooltip(s);
      }
    } else {
      if(app.connectMode) exitConnectMode();
      else if(focused) unpinTooltip();
    }
  }
  if(e.touches.length === 0) touchMode = null;
}, { passive: false });

// ════════════════════════════════════════════════════════════════════════
//   UI LAYER — floating menu, modals, settings, library management
// ════════════════════════════════════════════════════════════════════════

// (app state is declared near the top of this script — see "APP STATE")

// ── TOAST ───────────────────────────────────────────────────────────────
let toastTimer = null;
function toast(msg){
  const t = document.getElementById('toast');
  t.textContent = msg;
  t.classList.add('show');
  clearTimeout(toastTimer);
  toastTimer = setTimeout(()=>t.classList.remove('show'), 2200);
}

// ── PICTURE-FRAME EXPORT ────────────────────────────────────────────────
// Snapshot the current canvas to a PNG with a small watermark, then either
// hand it to the system Share sheet (mobile) or trigger a download (desktop).
async function shareCurrentView(){
  toast('Composing snapshot…');
  // Force one fresh render so the captured frame is exactly what's on screen
  // (avoids capturing a stale buffer if the tab was just unfocused).
  try { draw(performance.now()); } catch(e){}
  // Composite onto a new offscreen canvas with the watermark — keeps the live
  // canvas untouched.
  const out = document.createElement('canvas');
  out.width = canvas.width;
  out.height = canvas.height;
  const octx = out.getContext('2d');
  octx.drawImage(canvas, 0, 0);
  // Watermark: tiny italic "The Mind" + author name if signed in, in the corner
  const PAD = 28 * DPR;
  octx.font = (16 * DPR) + "px 'Cormorant Garamond', serif";
  octx.fillStyle = 'rgba(47,59,75,0.7)';
  octx.textBaseline = 'bottom';
  octx.textAlign = 'right';
  octx.fillText('Runaris', out.width - PAD, out.height - PAD - (12 * DPR));
  // Below in mono — book count and optional user name
  octx.font = (10 * DPR) + "px 'Figtree', sans-serif";
  octx.fillStyle = 'rgba(47,59,75,0.55)';
  const meta = STARS.length + ' books · ' + CENTRES.length + ' constellations'
             + (app.user ? ' · ' + (app.user.name || app.user.email) : '');
  octx.fillText(meta, out.width - PAD, out.height - PAD);
  // Export
  const filename = 'the-mind-' + new Date().toISOString().slice(0,10) + '.png';
  await new Promise(res => out.toBlob(async blob => {
    if(!blob){ toast('Snapshot failed'); res(); return; }
    // Try the Web Share API first (mobile-friendly). Requires HTTPS + a file.
    if(navigator.canShare && navigator.share){
      const file = new File([blob], filename, { type: 'image/png' });
      if(navigator.canShare({ files: [file] })){
        try {
          await navigator.share({
            files: [file],
            title: 'My Mind',
            text: "A cosmos of every book I've read.",
          });
          toast('Shared');
          res();
          return;
        } catch(e){
          // User cancelled, or share failed — fall through to download
        }
      }
    }
    // Fallback: trigger a download
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url; a.download = filename;
    document.body.appendChild(a); a.click(); a.remove();
    setTimeout(() => URL.revokeObjectURL(url), 1000);
    toast('Saved ' + filename);
    res();
  }, 'image/png'));
}

// ── BOTTOM DOCK ─────────────────────────────────────────────────────────
// Persistent action bar at the bottom: Add / Import / Customize / Settings /
// Profile. Replaces the earlier floating expand-on-tap menu.
document.querySelectorAll('#dock [data-action], #dock-profile').forEach(btn => {
  btn.addEventListener('click', e => {
    e.stopPropagation();
    const action = btn.dataset.action;
    if(action === 'cosmos'){
      // Back to the sky: close every overlay and selection
      closeModal();
      if(typeof timelapseEl !== 'undefined' && timelapseEl.classList.contains('open')) closeTimelapse();
      if(app.connectMode) exitConnectMode();
      if(focused) unpinTooltip();
      setNavActive('cosmos');
    } else if(action === 'library'){
      openModal('insights');
    } else if(action === 'profile'){
      openModal('profile');
    } else if(action === 'timelapse'){
      // Toggle the floating Time-lapse panel
      if(timelapseEl.classList.contains('open')) closeTimelapse();
      else openTimelapse();
    } else if(action === 'share'){
      shareCurrentView();
    } else {
      openModal(action);
    }
  });
});

function refreshProfileBadge(){
  const badge = document.getElementById('dock-profile');
  const letter = document.getElementById('avatar-letter');
  const name = document.getElementById('profile-name');
  if(!badge) return;
  if(app.user){
    badge.classList.remove('guest');
    letter.textContent = (app.user.name || app.user.email || 'U').charAt(0).toUpperCase();
    name.textContent = app.user.name || app.user.email;
  } else {
    badge.classList.add('guest');
    letter.textContent = '?';
    name.textContent = 'Sign in';
  }
  saveState();
}

// ── MODAL ROUTER ────────────────────────────────────────────────────────
const modal = document.getElementById('modal');
const modalTitle = document.getElementById('modal-title');
const modalTabs = document.getElementById('modal-tabs');
const modalBody = document.getElementById('modal-body');
document.getElementById('modal-close').addEventListener('click', closeModal);
modal.addEventListener('click', e => { if(e.target === modal) closeModal(); });
document.addEventListener('keydown', e => {
  if(e.key === 'Escape'){
    if(previewEl && previewEl.classList.contains('open')){ previewEl.classList.remove('open'); _scanPending = null; return; }
    if(scannerEl && scannerEl.classList.contains('open')){ closeScanner(); return; }
    if(document.getElementById('tooltip').classList.contains('editing')){ exitTooltipEditMode(false); return; }
    if(modal.classList.contains('open')) closeModal();
    else if(timelapseEl && timelapseEl.classList.contains('open')) closeTimelapse();
    else if(app.connectMode) exitConnectMode();
    else if(focused) unpinTooltip();
  }
});

let modalView = null;

function setNavActive(name){
  document.querySelectorAll('#dock .nav-btn[data-action]').forEach(b =>
    b.classList.toggle('active', b.dataset.action === name));
}
function closeModal(){
  modal.classList.remove('open');
  setNavActive('cosmos');
  // If the user was viewing the expanded book detail, the small tooltip is
  // gone and the mind is frozen — unfreeze and clear focus on close.
  if(modalView === 'book'){
    unpinTooltip();
  }
  modalView = null;
}

function openModal(view){
  modal.classList.add('open');
  setNavActive(view === 'insights' ? 'library' : 'none');
  modalTabs.innerHTML = '';
  modalView = view;
  if(view === 'add-book')      renderAddBook();
  else if(view === 'import')   renderImport();
  else if(view === 'insights') renderInsights();
  else if(view === 'customize')renderCustomize();
  else if(view === 'settings') renderSettings('app');
  else if(view === 'login')    renderLogin();
  else if(view === 'profile')  renderSettings('profile');
  else if(view === 'feedback') renderFeedback();
}

// ── PANEL: ADD BOOK ─────────────────────────────────────────────────────
function renderAddBook(){
  modalTitle.textContent = 'Add a book';
  modalBody.innerHTML = `
    <button class="btn" id="ab-scan" style="width:100%;margin-bottom:1rem;padding:0.85rem;display:flex;align-items:center;justify-content:center;gap:0.5rem">
      <span style="font-size:1rem">📷</span>
      <span>Scan ISBN with camera</span>
    </button>
    <div class="divider" style="margin:0.6rem 0 1rem">or enter manually</div>
    <div class="field"><label>Title</label><input type="text" id="ab-title" placeholder="The Name of the Rose"></div>
    <div class="field-row">
      <div class="field"><label>Author</label><input type="text" id="ab-author" placeholder="Umberto Eco"></div>
      <div class="field"><label>Year</label><input type="text" id="ab-year" placeholder="1980"></div>
      <div class="field"><label>Pages</label><input type="text" id="ab-pages" placeholder="320"></div>
    </div>
    <div class="field"><label>Genre</label>
      <select id="ab-genre">
        <option>Fiction</option><option>Sci-Fi</option><option>Fantasy</option><option>Mystery</option>
        <option>Horror</option><option>Romance</option><option>Philosophy</option><option>Science</option>
        <option>Non-Fiction</option><option>Poetry</option><option>History</option><option>Biography</option>
        <option>Other</option>
      </select>
    </div>
    <div class="field"><label>Subjects (comma-separated)</label>
      <input type="text" id="ab-subjects" placeholder="consciousness, AI, time">
      <div class="help">First subject decides which constellation the star joins. Pages determines star size.</div>
    </div>
    <div style="margin-top:1.4rem">
      <button class="btn btn-primary" id="ab-save">Add to mind</button>
      <button class="btn" id="ab-cancel">Cancel</button>
    </div>
  `;
  document.getElementById('ab-cancel').onclick = closeModal;
  document.getElementById('ab-scan').onclick = () => openScanner();
  document.getElementById('ab-save').onclick = () => {
    const title = document.getElementById('ab-title').value.trim();
    if(!title){ toast('Title is required'); return; }
    const book = {
      title,
      author: document.getElementById('ab-author').value.trim() || 'Unknown',
      year:   document.getElementById('ab-year').value.trim(),
      pages:  parseInt(document.getElementById('ab-pages').value, 10) || 0,
      genre:  document.getElementById('ab-genre').value,
      subjects: document.getElementById('ab-subjects').value.split(',').map(s=>s.trim()).filter(Boolean),
    };
    addBookToMind(book);
    closeModal();
    toast('Added "' + title + '" to the mind');
  };
  setTimeout(()=>document.getElementById('ab-title').focus(), 50);
}

// ── PANEL: IMPORT ───────────────────────────────────────────────────────
function renderImport(){
  modalTitle.textContent = 'Import library';
  modalBody.innerHTML = `
    <div class="help">Drop a <code>.csv</code> or <code>.json</code> file with your library. Each book needs <code>title</code>, and optionally <code>author</code>, <code>year</code>, <code>genre</code>, <code>subjects</code>.</div>
    <div class="field" style="margin-top:1rem">
      <label>Choose a file</label>
      <input type="file" id="im-file" accept=".csv,.json,application/json,text/csv" style="background:#fff;padding:10px;border:1px solid var(--line);border-radius:10px;width:100%;color:var(--ink);font-size:14px">
    </div>
    <div class="section-title">Or paste JSON directly</div>
    <div class="field">
      <textarea id="im-paste" placeholder='[{"title":"...","author":"...","subjects":["..."]}]'></textarea>
    </div>
    <div style="margin-top:1.4rem">
      <button class="btn btn-primary" id="im-go">Import</button>
      <button class="btn" id="im-cancel">Cancel</button>
    </div>
    <div class="section-title">CSV format</div>
    <div class="help">Header row: <code>title,author,year,genre,subjects</code><br>Subjects column uses semicolons or pipes between values: <code>consciousness;time;memory</code></div>
  `;
  document.getElementById('im-cancel').onclick = closeModal;
  document.getElementById('im-go').onclick = async () => {
    const file = document.getElementById('im-file').files[0];
    const pasted = document.getElementById('im-paste').value.trim();
    let books = null;
    try {
      if(file){
        const text = await file.text();
        if(file.name.toLowerCase().endsWith('.csv')) books = parseCSV(text);
        else books = JSON.parse(text);
      } else if(pasted){
        books = JSON.parse(pasted);
      } else {
        toast('Choose a file or paste JSON'); return;
      }
      if(books && books.books) books = books.books;
      if(!Array.isArray(books)) throw new Error('Not a list of books');
    } catch(err){
      toast('Could not parse: ' + err.message); return;
    }
    let added = 0;
    for(const b of books){
      if(b && b.title){ addBookToMind(normaliseBook(b)); added++; }
    }
    closeModal();
    toast('Imported ' + added + ' book' + (added===1?'':'s'));
  };
}

function parseCSV(text){
  const lines = text.split(/\r?\n/).filter(l => l.trim().length);
  if(lines.length < 2) return [];
  const header = lines[0].split(',').map(h => h.trim().toLowerCase());
  const out = [];
  for(let i = 1; i < lines.length; i++){
    const cells = splitCSVLine(lines[i]);
    const row = {};
    header.forEach((h, j) => row[h] = (cells[j]||'').trim());
    if(row.subjects) row.subjects = row.subjects.split(/[;|]/).map(s=>s.trim()).filter(Boolean);
    out.push(row);
  }
  return out;
}
function splitCSVLine(line){
  const out = []; let cur = ''; let inQ = false;
  for(let i=0;i<line.length;i++){
    const c = line[i];
    if(c==='"'){ if(inQ && line[i+1]==='"'){ cur+='"'; i++; } else inQ = !inQ; }
    else if(c===',' && !inQ){ out.push(cur); cur=''; }
    else cur += c;
  }
  out.push(cur);
  return out;
}
function normaliseBook(b){
  return {
    title: String(b.title || 'Untitled'),
    author: String(b.author || 'Unknown'),
    year: String(b.year || ''),
    pages: parseInt(b.pages || b.Pages || b.height || b.Height || 0, 10) || 0,
    genre: String(b.genre || 'Fiction'),
    subjects: Array.isArray(b.subjects) ? b.subjects : (b.subjects ? String(b.subjects).split(/[;|,]/).map(s=>s.trim()).filter(Boolean) : []),
  };
}

// ── PANEL: CUSTOMIZE ────────────────────────────────────────────────────
function renderCustomize(){
  // Modal-entry wrapper: sets the title and clears tabs, then fills the body.
  // The body-fill is also used by the Visuals tab inside Settings.
  modalTitle.textContent = 'Customize';
  modalTabs.innerHTML = '';
  renderCustomizeBody();
}
function renderCustomizeBody(){
  const v = app.visual;
  modalBody.innerHTML = `
    <div class="section-title">Filter by reading status</div>
    <div class="filter-chip-row" id="customize-filters">
      <div class="filter-chip ${app.statusFilter==='all'?'active':''}" data-filter="all">All <span class="count" id="cnt-all">0</span></div>
      <div class="filter-chip ${app.statusFilter==='reading'?'active':''}" data-filter="reading"><span class="dot" style="background:#2F3B4B"></span>Reading <span class="count" id="cnt-reading">0</span></div>
      <div class="filter-chip ${app.statusFilter==='finished'?'active':''}" data-filter="finished"><span class="dot" style="background:#5A7340"></span>Finished <span class="count" id="cnt-finished">0</span></div>
      <div class="filter-chip ${app.statusFilter==='unread'?'active':''}" data-filter="unread"><span class="dot" style="background:transparent;border:1.5px solid #7A7F76"></span>Unread <span class="count" id="cnt-unread">0</span></div>
      <div class="filter-chip ${app.statusFilter==='abandoned'?'active':''}" data-filter="abandoned"><span class="dot" style="background:#8E7F78"></span>Abandoned <span class="count" id="cnt-abandoned">0</span></div>
    </div>

    <div class="section-title">Animation</div>
    <div class="field">
      <div class="range-row"><label>Pulse rate</label><b id="v-pulseRate">${v.pulseRate.toFixed(1)}×</b></div>
      <input type="range" id="c-pulseRate" min="0" max="3" step="0.1" value="${v.pulseRate}">
    </div>
    <div class="field">
      <div class="range-row"><label>Star brightness</label><b id="v-starBrightness">${v.starBrightness.toFixed(1)}×</b></div>
      <input type="range" id="c-starBrightness" min="0.4" max="2" step="0.05" value="${v.starBrightness}">
    </div>
    <div class="field">
      <div class="range-row"><label>Auto-rotate (whole mind)</label><b id="v-rotationSpeed">${v.rotationSpeed.toFixed(2)}</b></div>
      <input type="range" id="c-rotationSpeed" min="0" max="0.4" step="0.01" value="${v.rotationSpeed}">
    </div>

    <div class="section-title">Constellations</div>
    <div class="field">
      <div class="range-row"><label>Gravity (cluster tightness)</label><b id="v-gravity">${v.gravity.toFixed(2)}×</b></div>
      <input type="range" id="c-gravity" min="0.3" max="2.5" step="0.05" value="${v.gravity}">
      <div class="help">Lower = stars drift far from centre · Higher = tight glowing knots.</div>
    </div>
    <div class="field">
      <div class="range-row"><label>Self-rotation speed</label><b id="v-constellationSpin">${v.constellationSpin.toFixed(2)}×</b></div>
      <input type="range" id="c-constellationSpin" min="0" max="4" step="0.05" value="${v.constellationSpin}">
      <div class="help">Each constellation spins on its own axis at its own rate.</div>
    </div>

    <div class="section-title">Nebula</div>
    <div class="field"><label><input type="checkbox" id="c-nebula" ${v.nebula?'checked':''}> Show cosmic nebula</label></div>
    <div class="field">
      <div class="range-row"><label>Nebula opacity</label><b id="v-nebulaOpacity">${v.nebulaOpacity.toFixed(2)}×</b></div>
      <input type="range" id="c-nebulaOpacity" min="0" max="2.5" step="0.05" value="${v.nebulaOpacity}">
    </div>
    <div class="field">
      <label>Nebula colour</label>
      <select id="c-nebulaColor">
        <option value="auto">Auto — mixed earth</option>
        <option value="blue">Slate</option>
        <option value="violet">Clay</option>
        <option value="teal">Sage</option>
        <option value="amber">Ochre</option>
        <option value="rose">Rose</option>
        <option value="mono">Stone</option>
        <option value="custom">Custom colour…</option>
      </select>
    </div>
    <div class="field" id="c-nebulaCustomRow" style="display:none">
      <label>Pick a colour</label>
      <input type="color" id="c-nebulaCustom" value="${v.nebulaCustom}" style="width:60px;height:36px;padding:0;border:1px solid var(--line);border-radius:8px;background:transparent">
    </div>

    <div class="section-title">Other</div>
    <div class="field"><label><input type="checkbox" id="c-breathing" ${v.breathing?'checked':''}> Sphere breathes</label></div>
    <div class="field"><label><input type="checkbox" id="c-synapses" ${v.synapses?'checked':''}> Constellation synapses</label></div>
    <div class="field"><label><input type="checkbox" id="c-showLabels" ${v.showLabels?'checked':''}> Constellation labels</label></div>

    <div class="section-title">Star palette</div>
    <div class="field"><select id="c-palette">
      <option value="default">Default — full spectrum</option>
      <option value="warm">Warm — amber &amp; rose</option>
      <option value="cool">Cool — blues &amp; violets</option>
      <option value="mono">Monochrome — silver white</option>
    </select></div>

    <div style="margin-top:1.4rem">
      <button class="btn btn-primary" id="c-done">Done</button>
      <button class="btn" id="c-reset">Reset</button>
    </div>
  `;
  document.getElementById('c-palette').value = v.paletteMode;
  document.getElementById('c-nebulaColor').value = v.nebulaColor;
  // show custom-colour picker only when 'custom' is selected
  function syncCustomRow(){
    document.getElementById('c-nebulaCustomRow').style.display =
      (app.visual.nebulaColor === 'custom') ? '' : 'none';
  }
  syncCustomRow();

  const bind = (id, key, fmt) => {
    const el = document.getElementById('c-'+id);
    el.addEventListener('input', () => {
      const val = el.type === 'checkbox' ? el.checked : parseFloat(el.value);
      app.visual[key] = val;
      const out = document.getElementById('v-'+id);
      if(out) out.textContent = fmt ? fmt(val) : val;
      saveState();
    });
  };
  bind('pulseRate','pulseRate', v=>v.toFixed(1)+'×');
  bind('starBrightness','starBrightness', v=>v.toFixed(1)+'×');
  bind('rotationSpeed','rotationSpeed', v=>v.toFixed(2));
  bind('gravity','gravity', v=>v.toFixed(2)+'×');
  bind('constellationSpin','constellationSpin', v=>v.toFixed(2)+'×');
  bind('nebulaOpacity','nebulaOpacity', v=>v.toFixed(2)+'×');
  bind('breathing','breathing');
  bind('nebula','nebula');
  bind('synapses','synapses');
  bind('showLabels','showLabels');

  // Filter chips: tap to set the active filter; recount on open.
  modalBody.querySelectorAll('.filter-chip').forEach(b => {
    b.addEventListener('click', () => setStatusFilter(b.dataset.filter));
  });
  refreshStatusCounts();

  document.getElementById('c-nebulaColor').addEventListener('change', e => {
    app.visual.nebulaColor = e.target.value;
    syncCustomRow();
    saveState();
  });
  document.getElementById('c-nebulaCustom').addEventListener('input', e => {
    app.visual.nebulaCustom = e.target.value;
    saveState();
  });
  document.getElementById('c-palette').addEventListener('change', e => {
    app.visual.paletteMode = e.target.value;
    applyPalette();
    saveState();
  });
  document.getElementById('c-done').onclick = closeModal;
  document.getElementById('c-reset').onclick = () => {
    Object.assign(app.visual, {
      pulseRate:1, breathing:true, nebula:true, synapses:true, showLabels:true,
      starBrightness:1, rotationSpeed:0, paletteMode:'default',
      gravity:1, nebulaOpacity:1, nebulaColor:'auto', nebulaCustom:'#8E7F78',
      constellationSpin:1,
    });
    applyPalette();
    renderCustomize();
  };
}

// ── PANEL: SETTINGS (tabbed) ────────────────────────────────────────────
function renderSettings(initialTab){
  modalTitle.textContent = 'Settings';
  modalTabs.innerHTML = '';
  const tabs = [
    ['profile','Profile'],['app','App'],['visuals','Visuals'],['library','Library'],['social','Social'],['about','About'],
  ];
  tabs.forEach(([id, label]) => {
    const t = document.createElement('div');
    t.className = 'panel-tab';
    t.textContent = label; t.dataset.tab = id;
    t.addEventListener('click', () => { switchTab(id); });
    modalTabs.appendChild(t);
  });
  switchTab(initialTab || 'app');
}
function switchTab(id){
  document.querySelectorAll('.panel-tab').forEach(t => t.classList.toggle('active', t.dataset.tab === id));
  if(id === 'profile') renderTabProfile();
  else if(id === 'app') renderTabApp();
  else if(id === 'visuals') renderCustomizeBody();
  else if(id === 'library') renderTabLibrary();
  else if(id === 'social') renderTabSocial();
  else if(id === 'about') renderTabAbout();
}

function renderTabProfile(){
  if(!app.user){
    modalBody.innerHTML = `
      <div class="help">You're browsing as a guest. Sign in to save your mindmap across devices.</div>
      <div style="margin-top:1rem"><button class="btn btn-primary" id="t-signin">Sign in</button></div>
    `;
    document.getElementById('t-signin').onclick = () => renderLogin();
    return;
  }
  modalBody.innerHTML = `
    <div style="display:flex;align-items:center;gap:1rem;margin-bottom:1.2rem">
      <div class="profile-btn" style="width:56px;height:56px;border-radius:28px;font-size:22px;cursor:default">${(app.user.name||'U').charAt(0).toUpperCase()}</div>
      <div>
        <div style="font-family:'Cormorant Garamond',serif;font-size:24px;font-style:italic;color:var(--ink)">${escapeHTML(app.user.name||'You')}</div>
        <div class="help" style="margin-top:0.2rem">${app.user.email||''}</div>
      </div>
    </div>
    <div class="section-title">Account</div>
    <div class="field"><label>Display name</label><input type="text" id="p-name" value="${app.user.name||''}"></div>
    <div class="field"><label>Email</label><input type="email" id="p-email" value="${app.user.email||''}" disabled></div>
    <div style="margin-top:1rem">
      <button class="btn btn-primary" id="p-save">Save</button>
      <button class="btn btn-danger" id="p-out">Sign out</button>
    </div>
  `;
  document.getElementById('p-save').onclick = () => {
    app.user.name = document.getElementById('p-name').value;
    refreshProfileBadge();
    toast('Profile saved');
  };
  document.getElementById('p-out').onclick = () => {
    app.user = null;
    refreshProfileBadge();
    toast('Signed out');
    switchTab('profile');
  };
}

function renderTabApp(){
  modalBody.innerHTML = `
    <div class="section-title">Display</div>
    <div class="field"><label><input type="checkbox" id="a-darkbg" checked disabled> Dark background (always on for planetarium)</label></div>
    <div class="field"><label><input type="checkbox" id="a-labels" checked> Show hovered labels</label></div>
    <div class="field"><label><input type="checkbox" id="a-reduce"> Reduce motion</label>
      <div class="help">Disables breathing and auto-rotation, lowers pulse rate.</div>
    </div>
    <div class="section-title">Notifications</div>
    <div class="field"><label><input type="checkbox" id="a-notif-friends"> When a friend updates their mindmap</label></div>
    <div class="field"><label><input type="checkbox" id="a-notif-rec"> Weekly reading recommendations</label></div>
    <div class="section-title">Data</div>
    <button class="btn btn-block" id="a-export">Export library (JSON)</button>
    <button class="btn btn-block btn-danger" id="a-clear">Clear local mindmap</button>
  `;
  document.getElementById('a-reduce').addEventListener('change', e => {
    if(e.target.checked){
      app.visual.breathing = false; app.visual.rotationSpeed = 0; app.visual.pulseRate = 0.4;
    } else {
      app.visual.breathing = true; app.visual.pulseRate = 1;
    }
  });
  document.getElementById('a-export').onclick = exportLibrary;
  document.getElementById('a-clear').onclick = () => {
    if(confirm('Clear all books from the mindmap? This cannot be undone.')) clearMind();
  };
}

function renderTabLibrary(){
  modalBody.innerHTML = `
    <div class="section-title">Stats</div>
    <div class="field" style="display:flex;gap:28px">
      <div><div class="stat-num">${STARS.length}</div><div class="help">books</div></div>
      <div><div class="stat-num">${CENTRES.length}</div><div class="help">constellations</div></div>
      <div><div class="stat-num">${EDGES.length}</div><div class="help">connections</div></div>
    </div>
    <div class="section-title">Quick actions</div>
    <button class="btn btn-block" data-route="add-book">＋ Add a book</button>
    <button class="btn btn-block" data-route="import">⇪ Import library</button>
    <button class="btn btn-block" id="l-export">↓ Export library (JSON)</button>
    <div class="section-title">Recent additions</div>
    <div id="l-recent"></div>
  `;
  modalBody.querySelectorAll('[data-route]').forEach(b =>
    b.addEventListener('click', () => openModal(b.dataset.route))
  );
  document.getElementById('l-export').onclick = exportLibrary;
  const recent = STARS.slice(-6).reverse();
  const recentDiv = document.getElementById('l-recent');
  recentDiv.innerHTML = recent.map(s => `
    <div style="padding:10px 0;border-bottom:1px solid var(--line)">
      <div class="lib-t">${escapeHTML(s.title)}</div>
      <div class="help" style="margin-top:2px">${escapeHTML(s.author)} · ${escapeHTML(s.subject)}</div>
    </div>`).join('') || '<div class="help">No books yet — add one to get started.</div>';
}

function renderTabSocial(){
  const services = [
    ['goodreads','Goodreads','#372213','#a09277','GR'],
    ['storygraph','The StoryGraph','#fbf6ee','#3b2f56','SG'],
    ['kindle','Amazon Kindle','#222e3d','#ffb400','K'],
    ['librarything','LibraryThing','#7b3f00','#fff','LT'],
  ];
  modalBody.innerHTML = `
    <div class="section-title">Connect a service</div>
    <div class="help" style="margin-bottom:0.8rem">Pull your reading history in from where you already track it.</div>
    ${services.map(([id,name,bg,fg,letter]) => {
      const c = app.connections[id];
      return `<div class="service-tile ${c?'connected':''}" data-svc="${id}">
        <div class="ico" style="background:${bg};color:${fg}">${letter}</div>
        <div class="name">${name}</div>
        <div class="status">${c?'Connected':'Connect'}</div>
      </div>`;
    }).join('')}
    <div class="section-title">Friends &amp; sharing</div>
    <button class="btn btn-block" id="s-share">Share my mindmap (read-only link)</button>
    <button class="btn btn-block" id="s-friends">Find friends by email</button>
    <button class="btn btn-block" id="s-public">Make profile public</button>
    <div class="help" style="margin-top:0.6rem">Sharing requires a signed-in account. (UI shells — no backend yet.)</div>
  `;
  modalBody.querySelectorAll('.service-tile').forEach(tile => {
    tile.addEventListener('click', () => {
      const id = tile.dataset.svc;
      app.connections[id] = !app.connections[id];
      toast(app.connections[id] ? 'Connected to ' + id : 'Disconnected from ' + id);
      saveState();
      renderTabSocial();
    });
  });
  document.getElementById('s-share').onclick = () =>
    app.user ? toast('Share link copied') : toast('Sign in to share');
  document.getElementById('s-friends').onclick = () =>
    app.user ? toast('No friends found yet') : toast('Sign in to find friends');
  document.getElementById('s-public').onclick = () =>
    app.user ? toast('Profile is now public') : toast('Sign in to publish');
}

function renderTabAbout(){
  modalBody.innerHTML = `
    <div style="font-family:'Cormorant Garamond',serif;font-size:32px;color:var(--ink);margin-bottom:10px">Runaris</div>
    <div class="help">A planetarium of everything you've ever read. Each book is a star; each subject a constellation.
      Connections pulse between books that share a thought.</div>
    <div class="section-title">Feedback</div>
    <div class="help" style="margin-bottom:0.6rem">What's working? What's broken? What would make this better?</div>
    <button class="btn btn-block" id="about-feedback">✉ Send feedback</button>
    <div class="section-title">Version</div>
    <div class="help">Runaris · v${APP_VERSION} · alpha</div>
    <div class="section-title">Credits</div>
    <div class="help">Built with HTML5 canvas. Cover art from OpenLibrary. No tracking, no backend.</div>
  `;
  document.getElementById('about-feedback').onclick = () => renderFeedback();
}

// ── PANEL: INSIGHTS ─────────────────────────────────────────────────────
// Auto-computed readings on the library. Each card is tappable: clicking
// performs a contextual action (filter, focus, open a book).
function renderInsights(){
  modalTitle.textContent = 'Library';
  modalTabs.innerHTML = '';
  if(!STARS.length){
    modalBody.innerHTML = `<div class="help">No books yet. Tap + to add your first one.</div>`;
    return;
  }
  // ── compute ──────────────────────────────────────────────────────────
  const total = STARS.length;
  const byAuthor = {};
  for(const s of STARS){ const a = s.author || 'Unknown'; byAuthor[a] = (byAuthor[a]||0)+1; }
  const authors = Object.entries(byAuthor).sort((a,b)=>b[1]-a[1]);
  const bySubject = {};
  for(const s of STARS){ const x = s.subject || 'unknown'; bySubject[x] = (bySubject[x]||0)+1; }
  const subjects = Object.entries(bySubject).sort((a,b)=>b[1]-a[1]);
  const statusCount = { unread:0, reading:0, finished:0, abandoned:0 };
  for(const s of STARS){ const st = peekStatus(s); if(statusCount[st]!==undefined) statusCount[st]++; }
  let biggest = null;
  for(const s of STARS){ if(s.pages && (!biggest || s.pages > biggest.pages)) biggest = s; }
  let topRated = null, topR = 0;
  for(const s of STARS){
    const r = (app.bookData[makeBookKey(s)] || {}).rating || 0;
    if(r > topR){ topR = r; topRated = s; }
  }
  const mra = authors[0] && authors[0][1] >= 2 ? authors[0] : null;
  const dom = subjects[0];
  const mostRecent = STARS[STARS.length - 1];

  // ── render helpers ───────────────────────────────────────────────────
  // verb is one of: 'filter', 'open-book', 'focus-author', 'focus-subject', null
  // payload is a small object passed to the dispatcher.
  function card(color, label, value, meta, verb, payload){
    const interactive = !!verb;
    const dataAttrs = interactive
      ? ` data-verb="${verb}" data-payload='${escapeAttr(JSON.stringify(payload||{}))}'`
      : '';
    return `<div class="insight-card${interactive?'':' empty'}"${dataAttrs}>
      <div class="insight-ico" style="color:${color}"></div>
      <div class="insight-body">
        <div class="insight-label">${escapeHTML(label)}</div>
        <div class="insight-value">${escapeHTML(value || '—')}</div>
        ${meta ? `<div class="insight-meta">${escapeHTML(meta)}</div>` : ''}
      </div>
    </div>`;
  }

  modalBody.innerHTML = `
    <input type="search" class="lib-search" id="lib-search" placeholder="Search titles, authors, subjects" aria-label="Search your library" value="${escapeAttr(app.searchQuery || '')}">
    <div style="display:flex;gap:8px;margin-bottom:6px">
      <button class="btn" id="ins-timelapse" style="flex:1;margin:0">Time-lapse</button>
      <button class="btn" id="ins-share" style="flex:1;margin:0">Share view</button>
    </div>
    <div class="section-title">Insights</div>

    ${mra
      ? card('#9A6C60', 'Most-read author', mra[0], mra[1] + ' books in your mind',
             'focus-author', { author: mra[0] })
      : card('#9A6C60', 'Most-read author', '—', 'Need 2+ books by the same author')}

    ${dom
      ? card('#6F838C', 'Dominant subject', dom[0],
             dom[1] + ' books · ' + Math.round(dom[1]/total*100) + '% of your mind',
             'focus-subject', { subject: dom[0] })
      : ''}

    ${biggest
      ? card('#D4A93E', 'Biggest book', biggest.title,
             biggest.author + ' · ' + biggest.pages + ' pages',
             'open-book', { key: makeBookKey(biggest) })
      : card('#D4A93E', 'Biggest book', '—', 'No page data')}

    ${topRated
      ? card('#9A6C60', 'Highest rated', topRated.title,
             topRated.author + ' · ' + topR + '/5 stars',
             'open-book', { key: makeBookKey(topRated) })
      : card('#9A6C60', 'Highest rated', '—', 'Rate some books to populate this')}

    ${mostRecent
      ? card('#5A7340', 'Most recently added', mostRecent.title, mostRecent.author,
             'open-book', { key: makeBookKey(mostRecent) })
      : ''}

    <div class="section-title">Your reading rhythm</div>
    ${statusCount.reading > 0
      ? card('#2F3B4B', 'Currently reading',
             statusCount.reading + ' book' + (statusCount.reading===1?'':'s'),
             'Tap to highlight just these',
             'filter', { filter:'reading' })
      : card('#2F3B4B', 'Currently reading', 'Nothing in progress',
             'Mark a book as "reading" from its detail panel')}

    ${statusCount.finished > 0
      ? card('#5A7340', 'Finished books', statusCount.finished + ' completed',
             Math.round(statusCount.finished/total*100) + '% of your library',
             'filter', { filter:'finished' })
      : card('#5A7340', 'Finished books', 'None yet marked', '')}

    ${statusCount.abandoned > 0
      ? card('#8E7F78', 'Started but abandoned', statusCount.abandoned + ' set aside',
             'Worth revisiting?',
             'filter', { filter:'abandoned' })
      : ''}

    ${card('#A5A79A', 'Untouched', statusCount.unread + ' unread',
           Math.round(statusCount.unread/total*100) + '% of your library still waits',
           'filter', { filter:'unread' })}

    <div class="section-title">By the numbers</div>
    <div style="display:flex;gap:1.4rem;flex-wrap:wrap">
      <div><div class="stat-num">${total}</div><div class="help">books</div></div>
      <div><div class="stat-num">${subjects.length}</div><div class="help">subjects</div></div>
      <div><div class="stat-num">${authors.length}</div><div class="help">authors</div></div>
    </div>
    <div class="section-title">All books</div>
    <div id="lib-list"></div>
  `;
  renderLibraryList();
  const libSearch = document.getElementById('lib-search');
  libSearch.addEventListener('keydown', e => e.stopPropagation());
  libSearch.addEventListener('input', () => {
    // Mirror into the cosmos search so the sky dims to matches too
    searchInput.value = libSearch.value;
    searchInput.dispatchEvent(new Event('input'));
    renderLibraryList();
  });

  // Wire card clicks through a single dispatcher
  modalBody.querySelectorAll('.insight-card[data-verb]').forEach(el => {
    el.addEventListener('click', () => {
      let payload = {};
      try { payload = JSON.parse(el.dataset.payload || '{}'); } catch(e){}
      runInsightAction(el.dataset.verb, payload);
    });
  });
  // Top-of-panel: Time-lapse and Share both close the modal first so the
  // cosmos is fully visible behind them.
  document.getElementById('ins-timelapse').addEventListener('click', () => {
    closeModal();
    openTimelapse();
  });
  document.getElementById('ins-share').addEventListener('click', () => {
    closeModal();
    // Give the canvas a frame to redraw before snapshotting
    setTimeout(() => shareCurrentView(), 60);
  });
}

// Alphabetical book list inside the Library panel, filtered by the search.
function renderLibraryList(){
  const el = document.getElementById('lib-list');
  if(!el) return;
  const q = app.searchQuery;
  const rows = STARS.filter(s => starMatchesSearch(s, q))
    .sort((a, b) => (a.title || '').localeCompare(b.title || ''));
  el.innerHTML = rows.map(s => `<button class="lib-row" data-key="${escapeAttr(makeBookKey(s))}">
      <span class="lib-dot" style="background:${s.color}"></span>
      <span><span class="lib-t">${escapeHTML(s.title)}</span><br><span class="lib-a">${escapeHTML(s.author || 'Unknown')} · ${escapeHTML(s.subject || '')}</span></span>
    </button>`).join('') || '<div class="help">No books match.</div>';
  el.querySelectorAll('.lib-row').forEach(b => b.addEventListener('click', () => {
    const star = STARS.find(s => makeBookKey(s) === b.dataset.key);
    if(star){ closeModal(); openBookDetail(star); }
  }));
}

// Dispatcher for insight-card actions.
function runInsightAction(verb, payload){
  if(verb === 'filter'){
    setStatusFilter(payload.filter);
    closeModal();
    toast('Filter: ' + payload.filter);
    return;
  }
  if(verb === 'open-book'){
    const star = STARS.find(s => makeBookKey(s) === payload.key);
    if(star){
      closeModal();
      openBookDetail(star);
    }
    return;
  }
  if(verb === 'focus-author'){
    // Use the existing search box to filter by author
    searchInput.value = payload.author;
    app.searchQuery = payload.author;
    searchWrap.classList.add('has-query');
    closeModal();
    toast('Showing: ' + payload.author);
    return;
  }
  if(verb === 'focus-subject'){
    searchInput.value = payload.subject;
    app.searchQuery = payload.subject;
    searchWrap.classList.add('has-query');
    closeModal();
    toast('Showing: ' + payload.subject);
    return;
  }
}

// Quick attribute-safe encode for inline JSON in HTML attributes.
function escapeAttr(s){
  return String(s).replace(/'/g,'&#39;').replace(/"/g,'&quot;');
}

// ── BARCODE SCANNER ─────────────────────────────────────────────────────
// Scan an ISBN-13 barcode with the device camera, look the book up on
// OpenLibrary, and show a confirmation card before adding.
//
// Detection strategy:
//   1. Native window.BarcodeDetector (Chrome / Android Chrome / Edge)
//   2. Fallback to @zxing/browser loaded from a CDN on-demand
//
// Privacy: the camera stream is stopped (all tracks) whenever the scanner
// closes — by user action OR a successful scan — and never re-used after.
const scannerEl      = document.getElementById('scanner');
const scannerVideo   = document.getElementById('scanner-video');
const scannerStatus  = document.getElementById('scanner-status');
const scannerCloseBtn = document.getElementById('scanner-close');
const previewEl      = document.getElementById('scan-preview');
const previewTitle   = document.getElementById('preview-title');
const previewAuthor  = document.getElementById('preview-author');
const previewMeta    = document.getElementById('preview-meta');
const previewIsbn    = document.getElementById('preview-isbn');
const previewCover   = document.getElementById('preview-cover');
const previewAdd     = document.getElementById('preview-add');
const previewRescan  = document.getElementById('preview-rescan');
const previewCancel  = document.getElementById('preview-cancel');

let _scanStream = null;
let _scanRAF    = null;
let _scanDetector = null;
let _scanZXingReader = null;
let _scanActive = false;
let _scanPending = null;   // book object awaiting Add confirmation

function setScanStatus(text, isError){
  scannerStatus.textContent = text;
  scannerStatus.classList.toggle('error', !!isError);
}

async function openScanner(){
  scannerEl.classList.add('open');
  setScanStatus('Initializing camera…');
  _scanActive = true;
  try {
    _scanStream = await navigator.mediaDevices.getUserMedia({
      video: { facingMode: { ideal: 'environment' } },
      audio: false,
    });
    scannerVideo.srcObject = _scanStream;
    await scannerVideo.play();
    setScanStatus('Looking for a barcode…');
    startScanLoop();
  } catch(err) {
    setScanStatus('Camera unavailable — check permissions', true);
  }
}

function closeScanner(){
  _scanActive = false;
  if(_scanRAF){ cancelAnimationFrame(_scanRAF); _scanRAF = null; }
  if(_scanStream){
    for(const t of _scanStream.getTracks()) t.stop();
    _scanStream = null;
  }
  try { scannerVideo.srcObject = null; } catch(e){}
  if(_scanZXingReader){
    try { _scanZXingReader.reset(); } catch(e){}
    _scanZXingReader = null;
  }
  scannerEl.classList.remove('open');
}
scannerCloseBtn.addEventListener('click', closeScanner);

async function startScanLoop(){
  // Native first
  if('BarcodeDetector' in window){
    try {
      _scanDetector = new window.BarcodeDetector({ formats: ['ean_13', 'ean_8', 'upc_a', 'code_128'] });
      const tick = async () => {
        if(!_scanActive) return;
        try {
          const codes = await _scanDetector.detect(scannerVideo);
          if(codes && codes.length){
            const raw = codes[0].rawValue || '';
            if(raw) return onBarcodeDetected(raw);
          }
        } catch(e){ /* ignore frame-level errors */ }
        _scanRAF = requestAnimationFrame(tick);
      };
      tick();
      return;
    } catch(e) { /* fall through to ZXing */ }
  }
  // Fallback: load ZXing from CDN once, then use its built-in viewfinder reader
  setScanStatus('Loading scanner library…');
  try {
    await loadZXing();
    const { BrowserMultiFormatReader } = window.ZXingBrowser || {};
    if(!BrowserMultiFormatReader) throw new Error('ZXing failed to load');
    _scanZXingReader = new BrowserMultiFormatReader();
    setScanStatus('Looking for a barcode…');
    _scanZXingReader.decodeFromVideoElement(scannerVideo, (result, err) => {
      if(!_scanActive) return;
      if(result){
        const raw = result.getText();
        if(raw) onBarcodeDetected(raw);
      }
    });
  } catch(e){
    setScanStatus('Scanner unavailable in this browser', true);
  }
}

function loadZXing(){
  return new Promise((resolve, reject) => {
    if(window.ZXingBrowser) return resolve();
    const s = document.createElement('script');
    s.src = 'https://unpkg.com/@zxing/browser@0.1.5/umd/zxing-browser.min.js';
    s.onload = () => resolve();
    s.onerror = () => reject(new Error('CDN load failed'));
    document.head.appendChild(s);
  });
}

async function onBarcodeDetected(code){
  // Pause scanning so the same code doesn't fire many times in a row
  _scanActive = false;
  if(_scanRAF){ cancelAnimationFrame(_scanRAF); _scanRAF = null; }
  if(_scanZXingReader){ try { _scanZXingReader.reset(); } catch(e){} _scanZXingReader = null; }
  // Only accept 10 or 13 digit ISBNs — strip non-digits and validate length
  const digits = String(code).replace(/[^0-9Xx]/g, '');
  if(digits.length !== 10 && digits.length !== 13){
    setScanStatus('Not an ISBN — keep aiming…');
    _scanActive = true;
    startScanLoop();
    return;
  }
  setScanStatus('ISBN ' + digits + ' — looking up…');
  // Stop the camera (we have what we need) and show the preview
  if(_scanStream){
    for(const t of _scanStream.getTracks()) t.stop();
    _scanStream = null;
  }
  try { scannerVideo.srcObject = null; } catch(e){}
  scannerEl.classList.remove('open');
  await showScanPreview(digits);
}

async function showScanPreview(isbn){
  previewEl.classList.add('open');
  previewTitle.textContent = 'Looking up…';
  previewAuthor.textContent = '';
  previewMeta.textContent = '';
  previewIsbn.textContent = 'ISBN ' + isbn;
  previewCover.style.backgroundImage = 'none';
  previewCover.classList.remove('empty');
  previewAdd.disabled = true;
  _scanPending = null;
  try {
    const book = await lookupISBN(isbn);
    if(!book){
      previewTitle.textContent = 'Not found';
      previewAuthor.textContent = 'OpenLibrary has no record for this ISBN.';
      previewMeta.textContent = '';
      previewCover.classList.add('empty');
      return;
    }
    _scanPending = book;
    previewTitle.textContent = book.title;
    previewAuthor.textContent = book.author;
    previewMeta.textContent = [book.year, book.pages ? book.pages + ' pages' : '', book.subjects[0]]
      .filter(Boolean).join(' · ');
    if(book._coverUrl){
      previewCover.style.backgroundImage = 'url("' + book._coverUrl + '")';
    } else {
      previewCover.classList.add('empty');
    }
    previewAdd.disabled = false;
  } catch(e){
    previewTitle.textContent = 'Lookup failed';
    previewAuthor.textContent = 'Check your connection and try again.';
    previewCover.classList.add('empty');
  }
}

// Hit OpenLibrary's books endpoint with the ISBN. Returns a normalized
// book object ready for addBookToMind, plus a _coverUrl for preview.
async function lookupISBN(isbn){
  const url = 'https://openlibrary.org/api/books?bibkeys=ISBN:' + encodeURIComponent(isbn) +
              '&jscmd=data&format=json';
  const res = await fetch(url);
  if(!res.ok) throw new Error('HTTP ' + res.status);
  const data = await res.json();
  const rec = data['ISBN:' + isbn];
  if(!rec) return null;
  const authors = (rec.authors || []).map(a => a.name).filter(Boolean);
  const subjects = (rec.subjects || []).map(s => (s.name || s)).filter(Boolean).slice(0, 6);
  const year = (rec.publish_date || '').match(/\d{4}/);
  return {
    title: rec.title || 'Untitled',
    author: authors.join(', ') || 'Unknown',
    year: year ? year[0] : '',
    pages: parseInt(rec.number_of_pages, 10) || 0,
    genre: 'Other',
    subjects: subjects.length ? subjects : ['general'],
    _coverUrl: (rec.cover && (rec.cover.large || rec.cover.medium || rec.cover.small)) || null,
  };
}

// Preview actions
previewAdd.addEventListener('click', () => {
  if(!_scanPending) return;
  const b = _scanPending;
  // Strip the preview-only _coverUrl before adding
  const { _coverUrl, ...book } = b;
  addBookToMind(book);
  // Seed coverCache so the new star already has its cover ready when opened
  if(_coverUrl){
    coverCache[(book.title || '') + '||' + (book.author || '')] = _coverUrl;
  }
  previewEl.classList.remove('open');
  _scanPending = null;
  // Batch mode: reopen the scanner for the next book.
  const batch = document.getElementById('scanner-batch');
  if(batch && batch.checked){
    toast('Added "' + book.title + '" · keep scanning');
    openScanner();
  } else {
    closeModal();
    toast('Added "' + book.title + '" to the mind');
  }
});
previewRescan.addEventListener('click', () => {
  previewEl.classList.remove('open');
  openScanner();
});
previewCancel.addEventListener('click', () => {
  previewEl.classList.remove('open');
  _scanPending = null;
});

// ── TIME-LAPSE ──────────────────────────────────────────────────────────
// A floating panel above the dock with a slider that scrubs through time.
// As the user drags, stars added AFTER the slider position vanish; their
// synapses go with them. Play button animates the scrub from earliest to
// now over ~8 seconds, letting the cosmos form constellation by
// constellation.
const timelapseEl = document.getElementById('timelapse');
const tlSlider    = document.getElementById('tl-slider');
const tlDate      = document.getElementById('tl-date');
const tlCount     = document.getElementById('tl-count');
const tlPlay      = document.getElementById('tl-play');
const tlReset     = document.getElementById('tl-reset');
const tlClose     = document.getElementById('tl-close');

let _tlPlayRAF = null;
let _tlPlayStart = 0;
const TL_PLAY_DURATION_MS = 8000;     // total animation length

function tlBounds(){
  // Earliest and latest dateAdded across the current library.
  // If we have no dated stars, fall back to "now"/"now" so the slider is inert.
  let lo = Infinity, hi = -Infinity;
  for(const s of STARS){
    if(!s.dateAdded) continue;
    if(s.dateAdded < lo) lo = s.dateAdded;
    if(s.dateAdded > hi) hi = s.dateAdded;
  }
  const now = Date.now();
  if(!isFinite(lo) || !isFinite(hi)){ lo = now - 86400000; hi = now; }
  // Always include "now" as the right edge so newly-added live books appear at full slider.
  if(hi < now) hi = now;
  return { lo, hi };
}

function tlValueToTimestamp(v){
  // slider value 0..1000 -> timestamp between lo and hi
  const { lo, hi } = tlBounds();
  return lo + (hi - lo) * (v / 1000);
}
function tlTimestampToValue(t){
  const { lo, hi } = tlBounds();
  if(hi === lo) return 1000;
  return Math.max(0, Math.min(1000, Math.round((t - lo) / (hi - lo) * 1000)));
}

function tlFormatDate(t){
  const d = new Date(t);
  const months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
  return months[d.getMonth()] + ' ' + d.getFullYear();
}

function setTimelapse(timestamp){
  // Setting timestamp to null returns to "present" (no filtering)
  if(timestamp == null){
    app.timelapseAt = null;
    tlDate.textContent = 'Now';
    tlCount.textContent = STARS.length + ' books';
    return;
  }
  app.timelapseAt = timestamp;
  tlDate.textContent = tlFormatDate(timestamp);
  let n = 0;
  for(const s of STARS){
    if(!s.dateAdded || s.dateAdded <= timestamp) n++;
  }
  tlCount.textContent = n + ' book' + (n === 1 ? '' : 's');
}

function openTimelapse(){
  timelapseEl.classList.add('open');
  // Start at the present
  tlSlider.value = 1000;
  setTimelapse(null);
}
function closeTimelapse(){
  timelapseEl.classList.remove('open');
  stopTimelapsePlay();
  // Always restore the live view when closing
  setTimelapse(null);
}

function stopTimelapsePlay(){
  if(_tlPlayRAF){ cancelAnimationFrame(_tlPlayRAF); _tlPlayRAF = null; }
  tlPlay.textContent = '▶ Play';
}
function startTimelapsePlay(){
  stopTimelapsePlay();
  tlPlay.textContent = '⏸ Pause';
  _tlPlayStart = performance.now();
  // Start the slider at the earliest moment
  tlSlider.value = 0;
  setTimelapse(tlValueToTimestamp(0));
  (function step(now){
    const t = Math.min(1, (now - _tlPlayStart) / TL_PLAY_DURATION_MS);
    const v = Math.round(t * 1000);
    tlSlider.value = v;
    setTimelapse(tlValueToTimestamp(v));
    if(t >= 1){
      stopTimelapsePlay();
      // Land on "now" cleanly so the present is restored
      setTimelapse(null);
      return;
    }
    _tlPlayRAF = requestAnimationFrame(step);
  })(performance.now());
}

tlSlider.addEventListener('input', () => {
  stopTimelapsePlay();
  const v = parseInt(tlSlider.value, 10);
  if(v >= 999){
    setTimelapse(null);          // present
  } else {
    setTimelapse(tlValueToTimestamp(v));
  }
});
tlPlay.addEventListener('click', () => {
  if(_tlPlayRAF) stopTimelapsePlay();
  else startTimelapsePlay();
});
tlReset.addEventListener('click', () => {
  stopTimelapsePlay();
  tlSlider.value = 1000;
  setTimelapse(null);
});
tlClose.addEventListener('click', closeTimelapse);

// ── PANEL: BOOK DETAIL (expanded from tooltip) ─────────────────────────
// ── STATUS FILTERS ──────────────────────────────────────────────────────
// Filter chips live inside the Customize panel now (rendered on demand).
// refreshStatusCounts is called from many mutation points — it tolerates
// the chips not being currently in the DOM.
function refreshStatusCounts(){
  const counts = { all: STARS.length, reading: 0, finished: 0, unread: 0, abandoned: 0 };
  for(const s of STARS){
    const st = peekStatus(s);
    if(counts[st] !== undefined) counts[st]++;
  }
  for(const k of Object.keys(counts)){
    const el = document.getElementById('cnt-' + k);
    if(el) el.textContent = counts[k];
  }
  saveState();
}
function setStatusFilter(name){
  app.statusFilter = name || 'all';
  document.querySelectorAll('.filter-chip').forEach(b =>
    b.classList.toggle('active', b.dataset.filter === app.statusFilter));
  saveState();
}

// ── HUD SEARCH ──────────────────────────────────────────────────────────
const searchInput = document.getElementById('hud-search-input');
const searchClear = document.getElementById('hud-search-clear');
const searchWrap  = document.getElementById('hud-search');
searchInput.addEventListener('input', () => {
  app.searchQuery = searchInput.value.trim();
  searchWrap.classList.toggle('has-query', app.searchQuery.length > 0);
});
searchClear.addEventListener('click', () => {
  searchInput.value = ''; app.searchQuery = '';
  searchWrap.classList.remove('has-query');
  searchInput.focus();
});
// Don't let canvas pan/zoom-keys steal typing
searchInput.addEventListener('keydown', e => e.stopPropagation());

refreshStatusCounts();
refreshProfileBadge();
// If a persisted palette mode is set, re-apply it so colors match the saved state.
if(app.visual.paletteMode && app.visual.paletteMode !== 'default'){
  applyPalette();
}

// ── FIRST-LAUNCH WELCOME ────────────────────────────────────────────────
// Show the welcome overlay if the user has never been here on this device.
// We treat "fresh state" as the trigger: nothing was loaded from storage AND
// the welcomed flag is false. Choosing a door dismisses the welcome and
// either routes to a specific action (scan/import/add) or just lets the
// user wander the demo.
const welcomeEl = document.getElementById('welcome');
function dismissWelcome(){
  welcomeEl.classList.remove('open');
  app.welcomed = true;
  saveState();
}
function showWelcome(){
  welcomeEl.classList.add('open');
}
welcomeEl.querySelectorAll('.welcome-door').forEach(door => {
  door.addEventListener('click', () => {
    const which = door.dataset.door;
    dismissWelcome();
    if(which === 'scan'){
      openModal('add-book');
      // Give the modal a tick to render, then auto-open the scanner
      setTimeout(() => openScanner(), 120);
    } else if(which === 'import'){
      openModal('import');
    } else if(which === 'add'){
      openModal('add-book');
    }
    // 'explore' just dismisses — the demo library is already loaded
  });
});
document.getElementById('welcome-signin').addEventListener('click', () => {
  dismissWelcome();
  openModal('login');
});
// Trigger: first launch (no saved state) OR explicitly never welcomed yet
if(!_loaded || !app.welcomed){
  showWelcome();
}

function openBookDetail(s){
  if(!s) return;
  const d = bookData(s);
  modalView = 'book';
  modal.classList.add('open');
  modalTitle.textContent = s.title;
  modalTabs.innerHTML = '';
  const c = s.color || '#6F838C';
  modalBody.innerHTML = `
    <div class="book-hero">
      <div class="book-cover-wrap" id="bd-cover-wrap">
        <div class="book-orb" style="color:${c}"></div>
        <div class="cover-spin"></div>
      </div>
      <div class="book-meta">
        <div style="font-family:'Cormorant Garamond',serif;font-style:italic;font-size:24px;color:var(--ink);line-height:1.15">${escapeHTML(s.title)}</div>
        <div class="by">${escapeHTML(s.author || 'Unknown')}${s.year ? ' · ' + escapeHTML(s.year) : ''}</div>
        <div class="yr">${escapeHTML(s.genre || '')} · ${escapeHTML(s.subject || '')}${s.pages ? ' · ' + s.pages + ' pages' : ''}</div>
        <div class="stars-row" id="bd-stars">
          ${[1,2,3,4,5].map(n => `<button class="star-btn ${n <= d.rating ? 'on':''}" data-r="${n}">★</button>`).join('')}
        </div>
      </div>
    </div>

    <div class="section-title">Reading status</div>
    <div class="chip-row" id="bd-status">
      ${['unread','reading','finished','abandoned'].map(st =>
        `<div class="chip ${d.status===st?'active':''}" data-st="${st}">${st}</div>`
      ).join('')}
    </div>

    <div class="section-title">Tags</div>
    <div class="chip-row">
      ${(s.subjects || []).map(x => `<div class="chip" style="cursor:default">${escapeHTML(x)}</div>`).join('') || '<div class="help">No tags</div>'}
    </div>

    <div class="section-title">Added to mind</div>
    <div class="field">
      <input type="date" id="bd-date" value="${dateInputValue(s.dateAdded)}">
      <div class="help">Used by the time-lapse to place this book in your reading history.</div>
    </div>

    <div class="section-title">Description</div>
    <div class="field">
      <textarea id="bd-desc" placeholder="A brief description, summary, or premise…" style="min-height:90px">${escapeHTML(d.description || '')}</textarea>
    </div>

    <div class="section-title">My notes</div>
    <div class="field">
      <textarea id="bd-notes" placeholder="Thoughts, quotes, why this matters to you…" style="min-height:140px">${escapeHTML(d.notes || '')}</textarea>
    </div>

    <div style="margin-top:1.4rem;display:flex;gap:0.5rem;flex-wrap:wrap">
      <button class="btn btn-primary" id="bd-save">Save</button>
      <button class="btn" id="bd-close">Close</button>
      <button class="btn btn-danger" id="bd-remove" style="margin-left:auto">Remove from mind</button>
    </div>
  `;
  // Kick off cover art fetch — show loading spinner, then fade the cover in
  // when it arrives. If lookup fails, the orb fallback stays visible.
  (function loadCover(){
    const wrap = document.getElementById('bd-cover-wrap');
    if(!wrap) return;
    wrap.classList.add('loading');
    // Capture current star to avoid race with another panel open
    const myKey = makeBookKey(s);
    Promise.resolve(fetchCover(s)).then(url => {
      // If user navigated away to a different book in the meantime, bail
      const stillOpen = document.getElementById('bd-cover-wrap');
      if(!stillOpen || stillOpen !== wrap) return;
      wrap.classList.remove('loading');
      if(!url) return;
      const img = new Image();
      img.alt = '';
      img.referrerPolicy = 'no-referrer';
      img.onload = () => {
        // Still mounted?
        if(!document.body.contains(wrap)) return;
        wrap.appendChild(img);
        // next frame: trigger transition
        requestAnimationFrame(() => {
          img.classList.add('loaded');
          wrap.classList.add('has-cover');
        });
      };
      img.onerror = () => { /* keep orb fallback */ };
      img.src = url;
    });
  })();
  // Rating
  modalBody.querySelectorAll('.star-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      const r = parseInt(btn.dataset.r, 10);
      d.rating = (d.rating === r) ? 0 : r;          // re-click clears
      modalBody.querySelectorAll('.star-btn').forEach((b, i) => {
        b.classList.toggle('on', (i + 1) <= d.rating);
      });
      saveState();
    });
  });
  // Status
  modalBody.querySelectorAll('#bd-status .chip').forEach(chip => {
    chip.addEventListener('click', () => {
      d.status = chip.dataset.st;
      modalBody.querySelectorAll('#bd-status .chip').forEach(c2 =>
        c2.classList.toggle('active', c2.dataset.st === d.status));
      refreshStatusCounts();
    });
  });
  // Save / close / remove
  document.getElementById('bd-save').onclick = () => {
    d.description = document.getElementById('bd-desc').value;
    d.notes       = document.getElementById('bd-notes').value;
    // dateAdded: parse the date input back into a timestamp. The input gives
    // us 'YYYY-MM-DD' (in local time); store as UTC midnight of that day.
    const dateVal = document.getElementById('bd-date').value;
    if(dateVal){
      const t = Date.parse(dateVal + 'T00:00:00');
      if(!isNaN(t)) s.dateAdded = t;
    }
    saveState();
    toast('Saved');
    closeModal();
  };
  document.getElementById('bd-close').onclick = closeModal;
  document.getElementById('bd-remove').onclick = () => {
    if(!confirm('Remove "' + s.title + '" from the mind?')) return;
    removeStarFromMind(s);
    closeModal();
    unpinTooltip();
    toast('Removed');
  };
}

// Remove a star and clean up edges + synapses + any orphaned constellation.
function removeStarFromMind(s){
  const idx = STARS.indexOf(s);
  if(idx < 0) return;
  STARS.splice(idx, 1);
  // re-index edges/synapses
  function fix(arr){
    for(let i = arr.length - 1; i >= 0; i--){
      const e = arr[i];
      if(e.a === idx || e.b === idx){ arr.splice(i, 1); continue; }
      if(e.a > idx) e.a--;
      if(e.b > idx) e.b--;
    }
  }
  fix(EDGES); fix(SYNAPSES);
  // re-index star.ci is unaffected (CENTRES order didn't change). But check
  // for orphan constellations (no stars left).
  const stillUsed = new Set(STARS.map(st => st.ci));
  // Don't actually remove orphan centres — they'd shift all ci values.
  // Just zero out their count for the HUD.
  CENTRES.forEach((c, i) => { c.count = 0; });
  STARS.forEach(st => { if(CENTRES[st.ci]) CENTRES[st.ci].count++; });
  refreshStatusCounts();
}

// ── PANEL: LOGIN ────────────────────────────────────────────────────────
// ── PANEL: FEEDBACK ─────────────────────────────────────────────────────
// Pre-fills a mailto: with the user's note plus a small environment footer.
function renderFeedback(){
  modalTitle.textContent = 'Send feedback';
  modalTabs.innerHTML = '';
  modalBody.innerHTML = `
    <div class="help" style="margin-bottom:1rem">What's working? What's broken? What would make this better?</div>
    <div class="field">
      <label>Type</label>
      <select id="fb-kind">
        <option value="Bug">Bug — something doesn't work</option>
        <option value="Idea">Idea — a feature I'd love</option>
        <option value="Praise">Praise — something I love</option>
        <option value="Confusion">Confusion — I don't understand X</option>
        <option value="Other">Other</option>
      </select>
    </div>
    <div class="field">
      <label>Your note</label>
      <textarea id="fb-body" placeholder="Tell me anything…" style="min-height:160px"></textarea>
    </div>
    <div class="field">
      <label>Your email (optional)</label>
      <input type="email" id="fb-from" placeholder="so I can write back" value="${escapeHTML(app.user && app.user.email || '')}">
    </div>
    <div style="margin-top:1.2rem">
      <button class="btn btn-primary" id="fb-send">Open my email</button>
      <button class="btn" id="fb-copy">Copy to clipboard</button>
      <button class="btn" id="fb-cancel">Cancel</button>
    </div>
    <div class="help" style="margin-top:1rem">
      Your note will be sent to <code>${FEEDBACK_EMAIL}</code> with a small footer noting your browser and app version (helps me fix bugs). Nothing else is collected.
    </div>
  `;
  setTimeout(() => document.getElementById('fb-body').focus(), 50);

  const buildMessage = () => {
    const kind = document.getElementById('fb-kind').value;
    const body = document.getElementById('fb-body').value.trim();
    const from = document.getElementById('fb-from').value.trim();
    const footer = [
      '',
      '— — — — —',
      'App version: ' + APP_VERSION,
      'Books in mind: ' + STARS.length,
      'Browser: ' + navigator.userAgent,
      'Sent: ' + new Date().toISOString(),
      from ? 'Reply to: ' + from : '',
    ].filter(Boolean).join('\n');
    return { kind, body, full: body + '\n\n' + footer };
  };

  document.getElementById('fb-cancel').onclick = closeModal;
  document.getElementById('fb-send').onclick = () => {
    const { kind, body, full } = buildMessage();
    if(!body){ toast('Add a note before sending'); return; }
    const subject = '[Runaris · ' + kind + '] feedback';
    const url = 'mailto:' + encodeURIComponent(FEEDBACK_EMAIL)
              + '?subject=' + encodeURIComponent(subject)
              + '&body='    + encodeURIComponent(full);
    // mailto: links don't always succeed (no email client configured).
    // We open in a hidden iframe-equivalent fallback if the direct
    // navigation appears to do nothing.
    window.location.href = url;
    toast('Opening your email app…');
    closeModal();
  };
  document.getElementById('fb-copy').onclick = async () => {
    const { full } = buildMessage();
    if(!full.trim().startsWith('—') && !document.getElementById('fb-body').value.trim()){
      toast('Add a note first'); return;
    }
    const composed = 'To: ' + FEEDBACK_EMAIL + '\nSubject: [Runaris] feedback\n\n' + full;
    try {
      await navigator.clipboard.writeText(composed);
      toast('Copied — paste into your email app');
    } catch(e){
      toast('Copy failed — your browser blocked clipboard access');
    }
  };
}

function renderLogin(){
  modalTitle.textContent = 'Sign in';
  modalTabs.innerHTML = '';
  modalBody.innerHTML = `
    <div class="help" style="margin-bottom:1rem">Sign in to save your mindmap across devices and connect with friends.</div>
    <button class="oauth-btn oauth-google" data-provider="Google"><div class="oauth-ico">G</div>Continue with Google</button>
    <button class="oauth-btn oauth-apple"  data-provider="Apple"><div class="oauth-ico"></div>Continue with Apple</button>
    <button class="oauth-btn oauth-email"  data-provider="Email"><div class="oauth-ico">@</div>Continue with email</button>
    <div class="divider">Or sign up</div>
    <div class="field"><label>Name</label><input type="text" id="li-name" placeholder="Your name"></div>
    <div class="field-row">
      <div class="field"><label>Email</label><input type="email" id="li-email" placeholder="you@somewhere.com"></div>
      <div class="field"><label>Password</label><input type="password" id="li-pw" placeholder="•••••••"></div>
    </div>
    <div style="margin-top:1rem">
      <button class="btn btn-primary" id="li-go">Create account</button>
      <button class="btn" id="li-cancel">Cancel</button>
    </div>
    <div class="help" style="margin-top:1rem">Note: these are visual shells — sign-in doesn't actually connect to anything yet.</div>
  `;
  modalBody.querySelectorAll('.oauth-btn').forEach(b => {
    b.addEventListener('click', () => {
      app.user = { name: 'Reader', email: b.dataset.provider.toLowerCase() + '@example.com', provider: b.dataset.provider };
      refreshProfileBadge();
      toast('Signed in with ' + b.dataset.provider);
      closeModal();
    });
  });
  document.getElementById('li-cancel').onclick = closeModal;
  document.getElementById('li-go').onclick = () => {
    const name = document.getElementById('li-name').value.trim();
    const email = document.getElementById('li-email').value.trim();
    if(!email){ toast('Email is required'); return; }
    app.user = { name: name || 'Reader', email };
    refreshProfileBadge();
    toast('Welcome, ' + (name || 'reader'));
    closeModal();
  };
}

// ── HELPERS: MUTATE THE MIND LIVE ───────────────────────────────────────
// Add a new star and rebuild the connection sets so it integrates immediately.
function addBookToMind(book){
  const primary = (book.subjects && book.subjects[0]) || 'general';
  // find or create constellation centre
  let centre = CENTRES.find(c => c.subject === primary);
  let ci = centre ? CENTRES.indexOf(centre) : -1;
  if(!centre){
    // place new constellation at a random point on the outer shell, opposite the densest area
    const t = Math.random();
    const phi = Math.acos(1 - 2 * t), theta = Math.random() * Math.PI * 2;
    const r = 320 + Math.random() * 50;
    const color = NEW_SUBJECT_COLOR();
    // every centre needs a rotation axis + spin speed for the in-loop math
    const axu = Math.random()*2-1, axt = Math.random()*Math.PI*2;
    const axs = Math.sqrt(Math.max(0, 1 - axu*axu));
    centre = {
      subject: primary,
      x: r * Math.sin(phi) * Math.cos(theta),
      y: r * Math.sin(phi) * Math.sin(theta),
      z: r * Math.cos(phi),
      color, origColor: color, count: 0,
      ax: Math.cos(axt)*axs, ay: Math.sin(axt)*axs, az: axu,
      spinSpeed: (0.05 + Math.random()*0.13) * (Math.random()<0.5?-1:1),
      spinPhase: Math.random()*Math.PI*2,
    };
    CENTRES.push(centre);
    ci = CENTRES.length - 1;
  }
  // drift around the centre (also store as ox/oy/oz so gravity + rotation work)
  const u = Math.random()*2-1, th = Math.random()*Math.PI*2;
  const s = Math.sqrt(Math.max(0,1-u*u));
  const dx = Math.cos(th)*s, dy = Math.sin(th)*s, dz = u;
  const dist = 60 * Math.pow(Math.random(), 1.3);
  const ox = dx*dist, oy = dy*dist, oz = dz*dist;
  // Star size from book.pages, normalized against the library's existing range
  let size;
  const pages = Number(book.pages || 0);
  if(pages > 0){
    let pmin = Infinity, pmax = 0;
    for(const st of STARS){ if(st.pages){ if(st.pages < pmin) pmin = st.pages; if(st.pages > pmax) pmax = st.pages; } }
    if(pmax > pmin){
      const tNorm = Math.max(0, Math.min(1, (pages - pmin) / (pmax - pmin)));
      size = 0.7 + tNorm * 1.5 + (Math.random()*0.16 - 0.08);
    } else {
      size = 1.0 + Math.random()*0.4;
    }
  } else {
    size = 1.0 + Math.random()*0.4;
  }
  const star = {
    kind: 'star', title: book.title, author: book.author, year: book.year,
    genre: book.genre, subject: primary, subjects: book.subjects,
    pages: pages,
    x: centre.x + ox, y: centre.y + oy, z: centre.z + oz,
    ox, oy, oz, ci,
    color: centre.color,
    origColor: centre.origColor || centre.color,
    size: Math.round(size * 1000) / 1000,
    phase: Math.random()*6.28,
    speed: 0.6 + Math.random()*1.0,
    dateAdded: Date.now(),
  };
  const newIdx = STARS.length;
  STARS.push(star);
  centre.count++;
  // build new edges + synapses incrementally
  for(let i = 0; i < newIdx; i++){
    const a = STARS[i];
    const sharesSubj = (a.subjects||[]).some(t => (star.subjects||[]).map(x=>x.toLowerCase()).includes(t.toLowerCase()));
    const sharesGenre = a.genre && a.genre === star.genre;
    const sharesAuthor = a.author && a.author === star.author;
    if(sharesSubj || sharesGenre || sharesAuthor){
      EDGES.push({ a: i, b: newIdx });
    }
  }
  // synapse: connect to nearest neighbour in same constellation
  let bestIdx = -1, bestD = Infinity;
  for(let i = 0; i < newIdx; i++){
    if(STARS[i].subject !== primary) continue;
    const d2 = (STARS[i].x-star.x)**2+(STARS[i].y-star.y)**2+(STARS[i].z-star.z)**2;
    if(d2 < bestD){ bestD = d2; bestIdx = i; }
  }
  if(bestIdx >= 0) SYNAPSES.push({ a: Math.min(bestIdx,newIdx), b: Math.max(bestIdx,newIdx) });
  refreshStatusCounts();
}

// Random pleasant colour for a new subject we don't have a hue for
const PALETTE_POOL = EARTH_COLORS;
function NEW_SUBJECT_COLOR(){ return PALETTE_POOL[Math.floor(Math.random()*PALETTE_POOL.length)]; }

function clearMind(){
  STARS.length = 0; CENTRES.length = 0; EDGES.length = 0; SYNAPSES.length = 0;
  clearPersistedState();
  refreshStatusCounts();
  toast('Mindmap cleared');
}

function exportLibrary(){
  const books = STARS.map(s => ({
    title: s.title, author: s.author, year: s.year, pages: s.pages || 0,
    genre: s.genre, subjects: s.subjects,
  }));
  const blob = new Blob([JSON.stringify(books, null, 2)], {type:'application/json'});
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url; a.download = 'mindmap-library.json';
  document.body.appendChild(a); a.click(); a.remove();
  setTimeout(()=>URL.revokeObjectURL(url), 1000);
  toast('Library exported');
}

// ── PALETTE MODE ────────────────────────────────────────────────────────
// Each star and centre carries an `origColor` set at generation time — that's
// the source of truth we restore to when the palette is reset.
const PALETTE_MAPS = {
  warm: ['#9A6C60','#D4A93E','#B99D84','#5A3A2C','#C4A398','#898270','#B08A67','#8E7F78'],
  cool: ['#6F838C','#5F6C78','#45505A','#2F3B4B','#7A8078','#8E9CA3','#5A7340','#414B38'],
  mono: ['#2F3B4B','#45505A','#5C635B','#7A7F76','#8E8E88','#6B6B6B','#4F4A45','#A5A79A'],
};
function applyPalette(){
  const mode = app.visual.paletteMode;
  if(mode === 'default'){
    for(const s of STARS)   s.color = s.origColor || s.color;
    for(const c of CENTRES) c.color = c.origColor || c.color;
    return;
  }
  const pool = PALETTE_MAPS[mode] || PALETTE_MAPS.cool;
  // map each subject to one colour in the pool deterministically
  const subjMap = {};
  CENTRES.forEach((c, i) => {
    const col = pool[i % pool.length];
    subjMap[c.subject] = col;
    c.color = col;
  });
  STARS.forEach(s => { s.color = subjMap[s.subject] || pool[0]; });
}

// ── HOOK CUSTOMIZE INTO LIVE RENDERING ──────────────────────────────────
// Slot live overrides into the existing draw loop via small global hooks:
//   * pulse spawn rate is multiplied by app.visual.pulseRate
//   * breath is bypassed if app.visual.breathing is false
//   * nebula skipped if app.visual.nebula is false
//   * synapses skipped if app.visual.synapses is false
//   * star size multiplied by app.visual.starBrightness
//   * camera rotated by app.visual.rotationSpeed every frame
//
// We patch by replacing a few key functions/values used in draw().
const _origBreathScale = breathScale;
breathScale = function(t){ return app.visual.breathing ? _origBreathScale(t) : 1; };

// auto-rotation tick — runs on every frame via a side-channel rAF
(function autoRotate(){
  if(!app.frozen) cam.rotY += app.visual.rotationSpeed * 0.016;
  requestAnimationFrame(autoRotate);
})();

// Patch pulse spawn cadence by wrapping spawnPulse and gating it
const _origSpawn = spawnPulse;
let _spawnGuard = 0;
spawnPulse = function(){
  // pulses are paused when the mind is frozen — the whole map stops thinking
  if(app.frozen) return;
  const rate = app.visual.pulseRate;
  if(rate <= 0) return;
  if(rate < 1){
    if(Math.random() > rate) return;
  }
  _origSpawn();
  if(rate > 1 && Math.random() < (rate - 1)) _origSpawn();
};

function escapeHTML(s){ return String(s).replace(/[&<>"']/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c])); }

// Format a ms-since-epoch timestamp as YYYY-MM-DD for <input type="date">.
// Returns '' if the input isn't a valid number.
function dateInputValue(ts){
  if(!ts || typeof ts !== 'number') return '';
  const d = new Date(ts);
  if(isNaN(d.getTime())) return '';
  const y = d.getFullYear();
  const m = String(d.getMonth() + 1).padStart(2, '0');
  const dd = String(d.getDate()).padStart(2, '0');
  return y + '-' + m + '-' + dd;
}

// ── PWA SERVICE WORKER ──────────────────────────────────────────────────
// Registers the cache layer so the app opens offline and qualifies as
// installable. Fails silently on file:// — service workers only work over
// HTTPS (or localhost), which Netlify provides.
if('serviceWorker' in navigator && location.protocol !== 'file:'){
  window.addEventListener('load', () => {
    navigator.serviceWorker.register('./sw.js').catch(() => { /* not fatal */ });
  });
}

</script>
</body>
</html>"""


if __name__ == "__main__":
    main()
