package todo

import (
	"strings"
	"time"

	"github.com/google/uuid"
	"golang.org/x/exp/slices"
)

type Todo struct {
	ID          uuid.UUID
	Description string
	CreatedAt   time.Time
	Complete    bool
}

type List struct {
	todos []Todo
}

func (s *List) Add(description string) {
	s.todos = append(s.todos, Todo{
		ID:          uuid.New(),
		Description: description,
		CreatedAt:   time.Now(),
	})
}

func (s *List) Rename(id uuid.UUID, name string) Todo {
	i := s.indexOf(id)
	s.todos[i].Description = name
	return s.todos[i]
}

func (s *List) Todos() []Todo {
	return s.todos
}

func (s *List) ToggleDone(id uuid.UUID) Todo {
	i := s.indexOf(id)
	s.todos[i].Complete = !s.todos[i].Complete
	return s.todos[i]
}

func (s *List) Delete(id uuid.UUID) {
	i := s.indexOf(id)
	s.todos = append(s.todos[:i], s.todos[i+1:]...)
}

func (s *List) ReOrder(ids []string) {
	var uuids []uuid.UUID
	for _, id := range ids {
		uuids = append(uuids, uuid.MustParse(id))
	}

	var newList []Todo
	for _, id := range uuids {
		newList = append(newList, s.todos[s.indexOf(id)])
	}

	s.todos = newList
}

func (s *List) Search(search string) []Todo {
	search = strings.ToLower(search)
	var results []Todo
	for _, todo := range s.todos {
		if strings.Contains(strings.ToLower(todo.Description), search) {
			results = append(results, todo)
		}
	}
	return results
}

func (s *List) Get(id uuid.UUID) Todo {
	return s.todos[s.indexOf(id)]
}

func (s *List) Empty() {
	s.todos = []Todo{}
}

func (s *List) indexOf(id uuid.UUID) int {
	return slices.IndexFunc(s.todos, func(todo Todo) bool {
		return todo.ID == id
	})
}
