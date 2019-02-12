# :pizza: Pizza Automaton

A while ago, I found myself going through the same repetitive process when ordering my pizzas, over and over every time I wanted a delivery of them.

At that moment, I was writing automation scripts at work for simulating user interaction with browsers, so then I realized, **why not automate my pizza orders and save myself some time?**

This repository contains the resulting code; a script that automates the order of my favorite pizzas from my favorite place, accounting even for day-dependent promotions.

## Built with

- **Python 3**.
- [**Selenium**](https://www.seleniumhq.org/) for simulating browser interaction.
- [**ChromeDriver**](http://chromedriver.chromium.org/) as browser agent.

## Structure

- `PizzaAutomation.py` contains the logic of the automation.
- `paths.json` contains CSS paths for all the elements with which the script interacts.
- `pizzas.json` is a map of names to indexes of the pizza menu.

## Run

The following considerations are relevant when running the script:

- Environment variables `DELIVERY_ADDRESS`, `DELIVERY_FLOOR` and `DELIVERY_DOOR` must be set before running.
- By default, the script asks for confirmation right before confirming the order (it displays final price, waiting time...). To skip this,  the script can be run with the `-y` parameter.