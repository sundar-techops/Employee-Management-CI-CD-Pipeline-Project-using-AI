package com.example.employeemanagementapi.repository;

import com.example.employeemanagementapi.model.Employee;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface EmployeeRepository extends JpaRepository<Employee, Long> {
    // JpaRepository gives us findAll(), findById(), save(), deleteById()
    // for FREE — no code needed here
}