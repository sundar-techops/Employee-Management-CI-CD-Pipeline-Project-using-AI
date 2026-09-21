package com.example.employeemanagementapi;

import com.example.employeemanagementapi.model.Employee;
import com.example.employeemanagementapi.repository.EmployeeRepository;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;

import static org.junit.jupiter.api.Assertions.*;

@SpringBootTest
class EmployeeManagementApiApplicationTests {

    @Autowired
    private EmployeeRepository employeeRepository;

    @Test
    void contextLoads() {
        // Tests that the Spring context starts without errors
    }

    @Test
    void testCreateAndRetrieveEmployee() {
        Employee emp = new Employee();
        emp.setName("Sundar Kumar");
        emp.setDepartment("DevOps");
        emp.setEmail("sundar@example.com");
        emp.setSalary(75000.0);

        Employee saved = employeeRepository.save(emp);

        assertNotNull(saved.getId());
        assertEquals("Sundar Kumar", saved.getName());
        assertEquals("DevOps", saved.getDepartment());
    }

    @Test
    void testDeleteEmployee() {
        Employee emp = new Employee();
        emp.setName("Test User");
        emp.setDepartment("IT");
        emp.setSalary(50000.0);
        Employee saved = employeeRepository.save(emp);

        employeeRepository.deleteById(saved.getId());
        assertFalse(employeeRepository.existsById(saved.getId()));
    }
}