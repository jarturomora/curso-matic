# Lesson 1: Introduction to the `if` Statement in Python

The `if` statement is used to execute a block of code only if a certain condition is true.

## Basic Syntax

The syntax of an `if` statement in Python is:

```python
if condition:
    # code to execute if condition is true
```

For example:

```python
age = 18
if age >= 18:
    print("You are an adult.")
```

## Using `if-else`

You can also use an `else` clause to run a block of code when the condition is false:

```python
age = 16
if age >= 18:
    print("You are an adult.")
else:
    print("You are a minor.")
```

## Using `if-elif-else`

When you need to check multiple conditions, use `elif` (short for "else if"):

```python
score = 85

if score >= 90:
    print("Grade: A")
elif score >= 80:
    print("Grade: B")
else:
    print("Keep studying!")
```

## Indentation Matters

Python relies on indentation (spacing) to define code blocks. Make sure you use consistent indentation, typically 4 spaces.

Incorrect example:

```python
if True:
print("This will cause an error")
```

Correct example:

```python
if True:
    print("This is properly indented")
```

## Summary

- Use `if` to check conditions.
- Combine with `else` or `elif` for more complex logic.
- Always pay attention to indentation in Python!

Happy coding!
