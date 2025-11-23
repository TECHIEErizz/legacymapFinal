package com.example;

import java.util.List;
import java.util.ArrayList;

public class UserManager {
    private List<String> users = new ArrayList<>();

    public void addUser(String name) {
        users.add(name);
        System.out.println("User added: " + name);
    }

    public List<String> getUsers() {
        return users;
    }
}
