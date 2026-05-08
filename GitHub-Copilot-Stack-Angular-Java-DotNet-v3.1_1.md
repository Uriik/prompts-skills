# 📗 GitHub Copilot - Estruturas Completas (v3.1)

**Stack:** Angular + Java + C# .NET Core  
**Data:** Maio 2026

---

## 🎯 Overview: 5 Componentes (Resumido)

```
INSTRUCTIONS (sempre) → AGENTS (@nome) → SKILLS (/nome ou automático)
                                      ↓
                                  PROMPTS (/cmd)
                                      ↓
                                  HOOKS (eventos)
```

---

## 📝 INSTRUCTIONS - Java/C# Exemplo

```markdown
# Project Standards - Java/.NET Core

## Tech Stack
- **Frontend:** Angular 17+, TypeScript 5.2+
- **Backend:** Java 21 LTS / C# .NET 8+
- **Testing:** JUnit 5 / xUnit, TestBed (Angular)
- **Build:** Maven/Gradle / MSBuild
- **Database:** SQL Server / PostgreSQL

## Naming Conventions

### Java
- Classes: `PascalCase` (UserManager, PaymentService)
- Methods: `camelCase` (getUserById, processPayment)
- Constants: `UPPER_SNAKE_CASE` (API_TIMEOUT, MAX_RETRIES)
- Packages: `lowercase.dotted` (com.company.domain)

### C# .NET
- Classes: `PascalCase` (UserManager, PaymentService)
- Properties: `PascalCase` (FirstName, EmailAddress)
- Methods: `PascalCase` (GetUserById, ProcessPayment)
- Constants: `UPPER_SNAKE_CASE` or `PascalCase` (ApiTimeout or API_TIMEOUT)
- Namespaces: `PascalCase.Dotted` (Company.Domain.Services)

### Angular
- Components: `PascalCase` (UserListComponent, LoginComponent)
- Selectors: `kebab-case` (app-user-list, app-login)
- Services: `PascalCase` (UserService, AuthService)
- Files: `kebab-case` (user-list.component.ts)

## Project Structure

```
Backend (Java):
src/main/java/com/company/
├── domain/          (DTOs, Entities)
├── service/         (Business logic)
├── repository/      (Data access)
├── controller/      (REST endpoints)
└── config/          (Spring/config)

Backend (C# .NET):
src/
├── Models/          (DTOs, Entities)
├── Services/        (Business logic)
├── Repositories/    (Data access)
├── Controllers/     (REST endpoints)
└── Configuration/   (DI, middleware)

Frontend (Angular):
src/
├── app/
│   ├── components/   (UI components)
│   ├── services/     (API calls)
│   ├── models/       (TypeScript interfaces)
│   ├── guards/       (Route guards)
│   └── interceptors/ (HTTP interceptors)
└── assets/          (images, styles)
```

## Mandatory Standards

- ✅ Java: Use pojos for immutable data (Java 16+)
- ✅ C#: Use nullable reference types (#nullable enable)
- ✅ Angular: Use standalone components (Angular 14+)
- ❌ Never use raw types or untyped responses
- ❌ No hardcoded strings (use constants/enums)
- ❌ No SQL injection (use parameterized queries)
```

---

## 🎭 AGENTS - Exemplos Completos

### Agent Developer (Java/C# focused)

```markdown
---
name: 'java-developer'
description: >
  Backend specialist in Java/C# .NET Core.
  Use for implementing APIs, services, data access, microservices.
  Keywords: java, backend, spring, api, service, endpoint.
tools:
  - read
  - search
  - edit
  - shell
model: 'claude-opus-4-6'
handoffs:
  - label: 'Unit Tests'
    agent: 'test-specialist'
    prompt: 'Create comprehensive JUnit 5 / xUnit tests'
    send: false
---

# Java/.NET Backend Developer

You are a senior backend engineer specializing in Java Spring Boot and C# .NET Core.

## Responsibilities

1. **REST API Implementation**
   ```yaml
   # Spring Boot Controller
   @RestController
   @RequestMapping("/api/users")
   public class UserController {
       @PostMapping
       public ResponseEntity<UserDTO> create(@RequestBody CreateUserRequest req) {
           // Implementation
       }
   }

   # C# .NET Controller
   [ApiController]
   [Route("api/[controller]")]
   public class UsersController : ControllerBase {
       [HttpPost]
       public async Task<ActionResult<UserDTO>> Create(CreateUserRequest req) {
           // Implementation
       }
   }
   ```

2. **Service Layer**
   ```java
   // Java
   @Service
   @Transactional
   public class UserService {
       public UserDTO createUser(CreateUserRequest req) {
           User user = new User(req.getName(), req.getEmail());
           return mapper.toDTO(repository.save(user));
       }
   }
   ```

   ```csharp
   // C#
   public class UserService : IUserService {
       public async Task<UserDTO> CreateUserAsync(CreateUserRequest req) {
           var user = new User { Name = req.Name, Email = req.Email };
           _repository.Add(user);
           await _unitOfWork.SaveChangesAsync();
           return _mapper.Map<UserDTO>(user);
       }
   }
   ```

3. **Error Handling**
   ```java
   // Java
   try {
       User user = service.getUser(id);
       return ResponseEntity.ok(user);
   } catch (EntityNotFoundException ex) {
       logger.error("User not found: {}", id, ex);
       return ResponseEntity.notFound().build();
   }
   ```

   ```csharp
   // C#
   try {
       var user = await _service.GetUserAsync(id);
       return Ok(user);
   } catch (EntityNotFoundException ex) {
       _logger.LogError(ex, "User not found: {UserId}", id);
       return NotFound();
   }
   ```

## Standards
- Use DTOs for API contracts
- Implement proper exception handling
- Use dependency injection (Spring/C# DI)
- Write parameterized SQL queries
- Add logging at method entry/exit
- Use database transactions for writes

## Tools
- #tool:search for finding similar services
- #tool:edit for creating new endpoints
- #tool:shell for running tests (mvn test / dotnet test)
```

### Agent Frontend (Angular)

```markdown
---
name: 'angular-developer'
description: >
  Frontend specialist in Angular.
  Use for components, services, pipes, directives, forms.
  Keywords: angular, frontend, component, service, form, typescript.
tools:
  - read
  - search
  - edit
  - shell
---

# Angular Frontend Developer

You are an expert Angular developer (17+, TypeScript 5+).

## Responsibilities

1. **Component Implementation**
   ```typescript
   // Standalone component (Angular 14+)
   import { Component, Input, Output, EventEmitter } from '@angular/core';
   import { CommonModule } from '@angular/common';
   
   @Component({
     selector: 'app-user-list',
     standalone: true,
     imports: [CommonModule],
     template: `
       <div *ngFor="let user of users">
         <p>{{ user.name }}</p>
         <button (click)="selectUser.emit(user)">Select</button>
       </div>
     `
   })
   export class UserListComponent {
     @Input() users: User[] = [];
     @Output() selectUser = new EventEmitter<User>();
   }
   ```

2. **Services with RxJS**
   ```typescript
   @Injectable({ providedIn: 'root' })
   export class UserService {
     private api = inject(HttpClient);
     
     getUsers(): Observable<User[]> {
       return this.api.get<User[]>('/api/users').pipe(
         catchError(err => {
           console.error('Error loading users', err);
           return of([]);
         })
       );
     }
   }
   ```

3. **Forms & Validation**
   ```typescript
   @Component({...})
   export class LoginComponent {
     fb = inject(FormBuilder);
     form = this.fb.group({
       email: ['', [Validators.required, Validators.email]],
       password: ['', [Validators.required, Validators.minLength(8)]]
     });
     
     onSubmit() {
       if (this.form.valid) {
         // Submit
       }
     }
   }
   ```

## Standards
- Use standalone components
- Leverage RxJS observables
- Implement proper error handling
- Use typed services
- Implement OnDestroy with takeUntilDestroyed
- Test with TestBed
```

---

## 🛠️ SKILLS - Exemplos Java/C#/Angular

### Skill: Unit Testing (Java/JUnit 5)

```markdown
---
name: 'java-unit-testing'
description: >
  Generate JUnit 5 unit tests with Mockito.
  Use when testing Java services, repositories, controllers.
  Keywords: junit, test, unit test, testing, mockito, test coverage.
allowed-tools:
  - shell
  - bash
context: fork
---

# Java Unit Testing with JUnit 5 & Mockito

## Before Starting
- [ ] JUnit 5 & Mockito dependencies added to pom.xml
- [ ] Service/repository class is clear
- [ ] Test environment configured

## Output Structure
1. **Test Class** — src/test/java/com/company/.../ServiceTest.java
2. **Coverage Report** — 80%+ minimum
3. **Summary** — tests created, coverage %

## Step 1: Analyze Service

```java
// Example service to test
@Service
public class PaymentService {
  private final PaymentRepository repo;
  
  public PaymentDTO processPayment(PaymentRequest req) 
      throws InvalidPaymentException {
    if (req.getAmount() <= 0) {
      throw new InvalidPaymentException("Amount must be positive");
    }
    Payment payment = new Payment(req);
    return mapper.toDTO(repo.save(payment));
  }
}
```

Identify:
- Input: PaymentRequest, dependencies
- Output: PaymentDTO, exceptions
- Branches: if (amount <= 0), if (valid), if (saved)

## Step 2: Create Test Cases

```
Happy Path: valid amount → saved payment
Edge: zero amount → exception
Edge: negative amount → exception
Error: database fails → exception
```

## Step 3: Generate Tests

```java
@ExtendWith(MockitoExtension.class)
class PaymentServiceTest {
  @Mock
  private PaymentRepository repository;
  
  @InjectMocks
  private PaymentService service;
  
  @Test
  void shouldProcessValidPayment() {
    // Arrange
    PaymentRequest request = new PaymentRequest(100.0);
    Payment savedPayment = new Payment(request);
    when(repository.save(any())).thenReturn(savedPayment);
    
    // Act
    PaymentDTO result = service.processPayment(request);
    
    // Assert
    assertNotNull(result);
    assertEquals(100.0, result.getAmount());
    verify(repository).save(any());
  }
  
  @Test
  void shouldThrowExceptionForZeroAmount() {
    PaymentRequest request = new PaymentRequest(0.0);
    
    assertThrows(InvalidPaymentException.class, 
      () -> service.processPayment(request));
  }
}
```

## Rules
- NEVER modify production code
- Use @Mock for dependencies
- Use @InjectMocks for service
- Test one behavior per test
- Minimum 80% coverage
- Name tests: shouldX_WhenY

## References
- [JUnit 5 Documentation](https://junit.org/junit5/)
- [Mockito Guide](https://javadoc.io/doc/org.mockito/mockito-core)
```

### Skill: Angular Component Testing

```markdown
---
name: 'angular-testing'
description: >
  Generate TestBed tests for Angular components.
  Use when testing components, services, pipes.
  Keywords: angular, testing, testbed, jasmine, component test.
allowed-tools:
  - shell
context: fork
---

# Angular Component Testing with TestBed & Jasmine

## Before Starting
- [ ] Angular testing dependencies installed
- [ ] Component is standalone or module declared
- [ ] Understand component @Input, @Output

## Step 1: Analyze Component

```typescript
@Component({
  selector: 'app-user-card',
  template: `
    <div>
      <h3>{{ user.name }}</h3>
      <button (click)="onDelete()">Delete</button>
    </div>
  `,
  standalone: true
})
export class UserCardComponent {
  @Input() user!: User;
  @Output() deleted = new EventEmitter<User>();
  
  onDelete() {
    this.deleted.emit(this.user);
  }
}
```

Identify: @Input (user), @Output (deleted), actions (onDelete)

## Step 2: Generate Tests

```typescript
describe('UserCardComponent', () => {
  let component: UserCardComponent;
  let fixture: ComponentFixture<UserCardComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [UserCardComponent]
    }).compileComponents();

    fixture = TestBed.createComponent(UserCardComponent);
    component = fixture.componentInstance;
  });

  it('should render user name', () => {
    component.user = { id: 1, name: 'John', email: 'j@example.com' };
    fixture.detectChanges();
    
    expect(fixture.nativeElement.textContent).toContain('John');
  });

  it('should emit deleted when delete clicked', () => {
    component.user = { id: 1, name: 'John', email: 'j@example.com' };
    spyOn(component.deleted, 'emit');
    
    const button = fixture.debugElement.query(By.css('button'));
    button.nativeElement.click();
    
    expect(component.deleted.emit).toHaveBeenCalledWith(component.user);
  });
});
```

## Rules
- Use TestBed.configureTestingModule
- Call fixture.detectChanges() after input change
- Test @Input rendering
- Test @Output events with spyOn
- Minimum 80% coverage
```

---

## 💬 PROMPTS - JSON/YAML para Estruturas Complexas

### Prompt 1: Generate Spring Boot Microservice

```markdown
---
description: >
  Generate complete Spring Boot REST API microservice with controller,
  service, repository, DTOs, entities, error handling.
  Use when scaffolding new microservice, creating domain module.
  Keywords: spring boot, microservice, api, controller, service, repository.
agent: 'java-developer'
model: 'claude-opus-4-6'
tools:
  - search/codebase
  - vscode/askQuestions
argument-hint: 'Service name and domain (e.g., UserService, PaymentService)'
---

# Generate Spring Boot Microservice

## Prerequisites
- Spring Boot 3.2+ configured
- Database configured
- Maven/Gradle setup

## Inputs Needed
1. **Service Name** (PascalCase): UserService, PaymentService
2. **Domain Entity** (YAML/JSON):
   ```yaml
   # Provide entity structure
   name: User
   fields:
     - name: id
       type: Long
       annotations: "@Id @GeneratedValue"
     - name: email
       type: String
       annotations: "@Column(unique=true) @Email"
     - name: firstName
       type: String
   ```

3. **Business Requirements** (Free text)

## Output Generation

### 1. Entity Class
```java
@Entity
@Table(name = "users")
@Data
@NoArgsConstructor
@AllArgsConstructor
public class User {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @Column(unique = true)
    @Email
    private String email;
    
    private String firstName;
}
```

### 2. DTO Classes
```java
@Data
public class CreateUserRequest {
    @NotBlank
    @Email
    private String email;
    
    @NotBlank
    @Size(min = 2)
    private String firstName;
}
```

### 3. Repository
```java
@Repository
public interface UserRepository extends JpaRepository<User, Long> {
    Optional<User> findByEmail(String email);
}
```

### 4. Service
```java
@Service
@Transactional
@RequiredArgsConstructor
public class UserService {
    private final UserRepository repository;
    private final UserMapper mapper;
    
    public UserDTO create(CreateUserRequest req) {
        User user = new User();
        user.setEmail(req.getEmail());
        user.setFirstName(req.getFirstName());
        return mapper.toDTO(repository.save(user));
    }
}
```

### 5. Controller
```java
@RestController
@RequestMapping("/api/users")
@RequiredArgsConstructor
public class UserController {
    private final UserService service;
    
    @PostMapping
    public ResponseEntity<UserDTO> create(@Valid @RequestBody CreateUserRequest req) {
        return ResponseEntity.status(201).body(service.create(req));
    }
}
```

## Standards Applied
- Use Lombok annotations (@Data, @RequiredArgsConstructor)
- Implement request validation (@Valid, @NotBlank)
- Use DTO pattern for API contracts
- Implement proper exception handling
- Use @Transactional for writes
- MapStruct for entity-DTO mapping

## References
- [Spring Data JPA](https://spring.io/projects/spring-data-jpa)
- [Spring Boot Best Practices](../../docs/SPRING_BOOT.md)
```

### Prompt 2: Generate C# .NET Service with DI

```markdown
---
description: >
  Generate C# .NET Core service with dependency injection,
  repositories, DTOs, controller, async/await patterns.
agent: 'java-developer'
argument-hint: 'Service name and entities'
---

# Generate C# .NET Core Service

## Structure Output

```csharp
// Models/User.cs
public class User {
    public int Id { get; set; }
    [EmailAddress]
    public string Email { get; set; } = null!;
    public string FirstName { get; set; } = null!;
}

// DTOs/CreateUserRequest.cs
public record CreateUserRequest(
    [EmailAddress] string Email,
    [StringLength(100)] string FirstName
);

// Repositories/IUserRepository.cs
public interface IUserRepository {
    Task<User?> GetByEmailAsync(string email);
    Task<User> CreateAsync(User user);
}

// Services/IUserService.cs
public interface IUserService {
    Task<UserDTO> CreateUserAsync(CreateUserRequest req);
}

// Services/UserService.cs
public class UserService : IUserService {
    private readonly IUserRepository _repository;
    private readonly IMapper _mapper;
    
    public UserService(IUserRepository repository, IMapper mapper) {
        _repository = repository;
        _mapper = mapper;
    }
    
    public async Task<UserDTO> CreateUserAsync(CreateUserRequest req) {
        var user = new User { Email = req.Email, FirstName = req.FirstName };
        await _repository.CreateAsync(user);
        return _mapper.Map<UserDTO>(user);
    }
}

// Controllers/UsersController.cs
[ApiController]
[Route("api/[controller]")]
public class UsersController(IUserService service) : ControllerBase {
    [HttpPost]
    public async Task<ActionResult<UserDTO>> Create(CreateUserRequest req) {
        var result = await service.CreateUserAsync(req);
        return CreatedAtAction(nameof(Create), result);
    }
}

// Program.cs (Dependency Injection Setup)
var builder = WebApplication.CreateBuilder(args);

builder.Services
    .AddScoped<IUserRepository, UserRepository>()
    .AddScoped<IUserService, UserService>()
    .AddAutoMapper(typeof(Program));

var app = builder.Build();
app.MapControllers();
app.Run();
```

## Standards
- Use records for immutable DTOs
- Enable nullable reference types
- Use async/await for I/O operations
- Implement proper DI in Program.cs
- Use ActionResult for REST responses
```

### Prompt 3: Generate Angular Component + Service

```markdown
---
description: >
  Generate Angular standalone component with service, typed data,
  reactive forms, error handling, RxJS patterns.
agent: 'angular-developer'
---

# Generate Angular Component + Service

## Input (YAML)
```yaml
component:
  name: UserListComponent
  selector: app-user-list
  features:
    - display users in table
    - search/filter
    - delete user
  
api:
  endpoint: /api/users
  methods:
    - GET /api/users
    - DELETE /api/users/{id}
```

## Output

```typescript
// Models
export interface User {
  id: number;
  email: string;
  firstName: string;
}

// Service
@Injectable({ providedIn: 'root' })
export class UserService {
  private api = inject(HttpClient);
  
  getUsers(): Observable<User[]> {
    return this.api.get<User[]>('/api/users').pipe(
      catchError(err => {
        console.error('Failed to load users', err);
        return of([]);
      })
    );
  }
  
  deleteUser(id: number): Observable<void> {
    return this.api.delete<void>(`/api/users/${id}`);
  }
}

// Component
@Component({
  selector: 'app-user-list',
  standalone: true,
  imports: [CommonModule, FormsModule],
  template: `
    <div>
      <input [(ngModel)]="searchTerm" placeholder="Search...">
      <table>
        <tr *ngFor="let user of filteredUsers">
          <td>{{ user.firstName }}</td>
          <td>{{ user.email }}</td>
          <td><button (click)="delete(user.id)">Delete</button></td>
        </tr>
      </table>
    </div>
  `
})
export class UserListComponent implements OnInit {
  userService = inject(UserService);
  users: User[] = [];
  searchTerm = '';
  
  ngOnInit() {
    this.userService.getUsers()
      .pipe(takeUntilDestroyed())
      .subscribe(users => this.users = users);
  }
  
  get filteredUsers(): User[] {
    return this.users.filter(u => 
      u.email.includes(this.searchTerm)
    );
  }
  
  delete(id: number) {
    this.userService.deleteUser(id)
      .pipe(takeUntilDestroyed())
      .subscribe(() => {
        this.users = this.users.filter(u => u.id !== id);
      });
  }
}
```

## Standards
- Standalone components (Angular 14+)
- Typed data with interfaces
- RxJS with takeUntilDestroyed
- Proper error handling
- Two-way binding for forms
```

---

## 🏗️ Estruturas Complexas em JSON/YAML

### Config 1: Spring Boot Configuration (YAML)

```yaml
---
spring:
  application:
    name: user-service
  datasource:
    url: jdbc:mysql://localhost:3306/users_db
    username: ${DB_USER}
    password: ${DB_PASSWORD}
    hikari:
      maximum-pool-size: 20
      minimum-idle: 5
      connection-timeout: 30000
  jpa:
    hibernate:
      ddl-auto: validate
    properties:
      hibernate:
        dialect: org.hibernate.dialect.MySQL8Dialect
        format_sql: true
        jdbc:
          batch_size: 20
  mvc:
    throw-exception-if-no-handler-found: true
  web:
    resources:
      add-mappings: false

server:
  port: 8080
  servlet:
    context-path: /api
  error:
    include-message: always
    include-binding-errors: always

logging:
  level:
    root: INFO
    com.company: DEBUG
  pattern:
    console: "%d{yyyy-MM-dd HH:mm:ss} [%thread] %-5level %logger{36} - %msg%n"

# Prompts para Copilot:
# "Configure Spring Boot application with these settings"
# "Add database connection pooling with HikariCP"
```

### Config 2: .NET Core Configuration (JSON)

```json
{
  "Logging": {
    "LogLevel": {
      "Default": "Information",
      "Microsoft": "Warning",
      "Company.Domain": "Debug"
    }
  },
  "ConnectionStrings": {
    "DefaultConnection": "Server=localhost;Database=UsersDb;User=sa;Password=${DB_PASSWORD};"
  },
  "Database": {
    "ConnectionPoolSize": 20,
    "CommandTimeout": 30
  },
  "Jwt": {
    "SecretKey": "${JWT_SECRET}",
    "Audience": "company-api",
    "Issuer": "company-auth"
  },
  "AllowedHosts": "*"
}
```

### Config 3: Angular Environment Configuration (TypeScript)

```typescript
// environment.ts
export const environment = {
  production: false,
  apiUrl: 'http://localhost:8080/api',
  apiTimeout: 30000,
  auth: {
    tokenKey: 'access_token',
    refreshTokenKey: 'refresh_token'
  },
  features: {
    enableLogging: true,
    enableDevTools: true
  }
};

// environment.prod.ts
export const environment = {
  production: true,
  apiUrl: 'https://api.company.com',
  apiTimeout: 60000,
  auth: {
    tokenKey: 'access_token',
    refreshTokenKey: 'refresh_token'
  },
  features: {
    enableLogging: false,
    enableDevTools: false
  }
};
```

---

## 📊 Matriz Stack Específicas

```
┌─────────────────────────────────────────────────────────────┐
│            TECNOLOGIAS E PADRÕES POR CAMADA                │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│ FRONTEND (Angular 17+)                                     │
│ ├─ Standalone Components                                  │
│ ├─ TestBed + Jasmine for testing                         │
│ ├─ RxJS Observables + takeUntilDestroyed                 │
│ ├─ Reactive Forms (FormBuilder, FormGroup)               │
│ └─ HTTP Client with Interceptors                         │
│                                                             │
│ BACKEND JAVA (Spring Boot 3.2+)                           │
│ ├─ JPA/Hibernate for ORM                                 │
│ ├─ Spring Data repositories                              │
│ ├─ Service layer with @Transactional                     │
│ ├─ REST Controllers with @RestController                 │
│ ├─ JUnit 5 + Mockito for testing                         │
│ └─ Maven/Gradle for build                                │
│                                                             │
│ BACKEND C# .NET (8+)                                       │
│ ├─ Entity Framework Core for ORM                         │
│ ├─ Repository pattern (interface-based)                  │
│ ├─ Service pattern with DI                               │
│ ├─ API Controllers                                       │
│ ├─ xUnit + Moq for testing                               │
│ ├─ Records for DTOs                                      │
│ └─ Nullable reference types enabled                      │
│                                                             │
│ DATABASE                                                   │
│ ├─ SQL Server (C#)                                       │
│ ├─ PostgreSQL / MySQL (Java)                             │
│ └─ Parameterized queries (NO SQL injection)              │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 🎯 Checklist de Setup Completo

```
PROJECT SETUP:

INSTRUCTIONS:
  ☐ Stack definido (Java/Spring Boot 3.2+, C#/.NET 8+, Angular 17+)
  ☐ Naming conventions claras (Java: PascalCase methods, C#: PascalCase props)
  ☐ Project structure defined
  ☐ Build commands documentados (mvn test, dotnet test, npm test)
  ☐ 50 linhas máximo

AGENTS:
  ☐ @java-developer (Spring Boot, JPA, REST APIs)
  ☐ @dotnet-developer (C#, Entity Framework, DI)
  ☐ @angular-developer (Components, Services, RxJS)
  ☐ Handoffs entre agents

SKILLS:
  ☐ /java-unit-testing (JUnit 5, Mockito)
  ☐ /dotnet-testing (xUnit, Moq)
  ☐ /angular-testing (TestBed, Jasmine)
  ☐ /spring-boot-scaffold (microservice generation)
  ☐ /dotnet-scaffold (service with DI)

PROMPTS:
  ☐ /generate-spring-service
  ☐ /generate-dotnet-service
  ☐ /generate-angular-component
  ☐ /generate-rest-api

HOOKS:
  ☐ preToolUse: check secrets, validate code
  ☐ postToolUse: run linting (ESLint, prettier, checkstyle)
  ☐ sessionStart: validate project health

TOKENS:
  ☐ Instructions: ~50 tokens
  ☐ Agent: ~50 tokens/sessão
  ☐ Skills: ~250 tokens se usado
  ☐ Total: ~350 tokens/sessão (70-80% economia)
```

---

## 🔄 Workflow Exemplo: Criar API REST (Java)

```
1. Seleciona @java-developer
2. Digita: "Create REST API for users (create, list, delete)"
3. Copilot oferece prompt /generate-spring-service
4. Usuario confirma e fornece entity structure em YAML
5. Skill gera:
   - Entity (User.java)
   - Repository (UserRepository.java)
   - DTO (CreateUserRequest, UserDTO)
   - Service (UserService.java)
   - Controller (UserController.java)
   - Testes (UserServiceTest.java com JUnit 5)
6. Hooks executam:
   - Prettier + ESLint
   - Maven compile + test
7. Usuario usa handoff para "Create Unit Tests"
8. Test-specialist agent cria testes completos (80%+ coverage)
9. Pronto para commit!

TEMPO: ~5-10 minutos
TOKENS: ~600 total
CÓDIGO GERADO: ~1000+ linhas
```

---

**Documento v3.1 - Angular + Java + C# .NET Core com JSON/YAML**

**Pronto para implementação em Maio 2026**
