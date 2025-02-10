package pro.demo.springrequest;

import jakarta.validation.constraints.*;

public class UserRequest {
    @NotBlank(message = "Name cannot be blank")
    @Size(min = 2, max = 50, message = "Name must be between 2-50 characters")
    private String name;

    @Email(message = "Invalid email format")
    @NotNull(message = "Email cannot be null")
    private String email;

    @Min(value = 18, message = "Age must be at least 18")
    @Max(value = 120, message = "Age cannot exceed 120")
    private int age;

    // Getters and Setters
    public String getName() { return name; }
    public void setName(String name) { this.name = name; }
    public String getEmail() { return email; }
    public void setEmail(String email) { this.email = email; }
    public int getAge() { return age; }
    public void setAge(int age) { this.age = age; }
}
