package com.example.employeemanagementapi.controller;

import com.example.employeemanagementapi.model.Employee;
import com.example.employeemanagementapi.repository.EmployeeRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Optional;

@RestController
@RequestMapping("/api/employees")
public class EmployeeController {

    @Autowired
    private EmployeeRepository employeeRepository;

    // GET all employees
    @GetMapping
    public List<Employee> getAllEmployees() {
        return employeeRepository.findAll();
    }

    // GET single employee by ID
    @GetMapping("/{id}")
    public ResponseEntity<Employee> getEmployeeById(@PathVariable Long id) {
        Optional<Employee> employee = employeeRepository.findById(id);
        if (employee.isPresent()) {
            return ResponseEntity.ok(employee.get());
        } else {
            return ResponseEntity.notFound().build();
        }
    }

    // POST - create new employee
    @PostMapping
    public Employee createEmployee(@RequestBody Employee employee) {
        return employeeRepository.save(employee);
    }

    // PUT - update existing employee
    @PutMapping("/{id}")
    public ResponseEntity<Employee> updateEmployee(@PathVariable Long id,
                                                    @RequestBody Employee updatedEmployee) {
        if (!employeeRepository.existsById(id)) {
            return ResponseEntity.notFound().build();
        }
        updatedEmployee.setId(id);
        return ResponseEntity.ok(employeeRepository.save(updatedEmployee));
    }

    // DELETE employee
    @DeleteMapping("/{id}")
    public ResponseEntity<Void> deleteEmployee(@PathVariable Long id) {
        if (!employeeRepository.existsById(id)) {
            return ResponseEntity.notFound().build();
        }
        employeeRepository.deleteById(id);
        return ResponseEntity.ok().build();
        THIS_WILL_FAIL;
    }
}