(define (domain household)
  (:requirements :typing)

  (:types
    thing
    character - thing
    room - thing
    object - thing
    container - object
    furniture - object
  )

  (:predicates
    ;; Character location
    (in ?c - character ?r - room)
    (at ?c - character ?o - object)

    ;; Object location
    (on ?o - object ?s - object)
    (inside ?o - object ?c - container)
    (close_char_object ?c - character ?o - object)
    (facing ?o1 - object ?o2 - object)

    ;; Object states
    (open_state ?o - object)
    (closed_state ?o - object)
    (on_state ?o - object)
    (off_state ?o - object)
    (grabbable ?o - object)
    (sittable ?o - object)
    (switch ?o - object)

    ;; Character holding object
    (holding_rh ?c - character ?o - object)
    (holding_lh ?c - character ?o - object)

    ;; Character sitting
    (sitting ?c - character ?obj - object)
    (is_sitting ?c - character)
  )

  ;; ===================== Actions =====================

  ;; Walk to a room
  (:action walk_to_room
    :parameters (?c - character ?r - room)
    :precondition (not (is_sitting ?c))
    :effect (in ?c ?r)
  )

  ;; Walk to an object
  (:action walk_to_object
    :parameters (?c - character ?o - object)
    :precondition (not (is_sitting ?c))
    :effect (at ?c ?o)
  )

  ;; Run to a room
  (:action run_to_room
    :parameters (?c - character ?r - room)
    :precondition (not (is_sitting ?c))
    :effect (in ?c ?r)
  )

  ;; Run to an object
  (:action run_to_object
    :parameters (?c - character ?o - object)
    :precondition (not (is_sitting ?c))
    :effect (at ?c ?o)
  )

  ;; Sit on an object
  (:action sit_on_object
    :parameters (?c - character ?obj - object)
    :precondition (and
      (not (is_sitting ?c))
      (close_char_object ?c ?obj)
      (sittable ?obj)
    )
    :effect (and
      (sitting ?c ?obj)
      (is_sitting ?c)
    )
  )

  ;; Stand up
  (:action stand_up
    :parameters (?c - character ?obj - object)
    :precondition (sitting ?c ?obj)
    :effect (and
      (not (sitting ?c ?obj))
      (not (is_sitting ?c))
    )
  )

  ;; Grab an object
  (:action grab_object
    :parameters (?c - character ?obj - object)
    :precondition (and
      (grabbable ?obj)
      (close_char_object ?c ?obj)
      (not (holding_rh ?c ?obj))
      (not (holding_lh ?c ?obj))
    )
    :effect (holding_rh ?c ?obj)
  )

  ;; Open an object
  (:action open_object
    :parameters (?c - character ?obj - object)
    :precondition (and
      (closed_state ?obj)
      (close_char_object ?c ?obj)
    )
    :effect (and
      (open_state ?obj)
      (not (closed_state ?obj))
    )
  )

  ;; Close an object
  (:action close_object
    :parameters (?c - character ?obj - object)
    :precondition (and
      (open_state ?obj)
      (close_char_object ?c ?obj)
    )
    :effect (and
      (closed_state ?obj)
      (not (open_state ?obj))
    )
  )

  ;; Put object on another object
  (:action put_object_on
    :parameters (?c - character ?obj - object ?target - object)
    :precondition (or (holding_rh ?c ?obj) (holding_lh ?c ?obj))
    :effect (and
      (not (holding_rh ?c ?obj))
      (not (holding_lh ?c ?obj))
      (on ?obj ?target)
    )
  )

  ;; Put object inside another object
  (:action put_object_in
    :parameters (?c - character ?obj - object ?container - container)
    :precondition (and
      (or (holding_rh ?c ?obj) (holding_lh ?c ?obj))
      (close_char_object ?c ?container)
      (not (closed_state ?container))
    )
    :effect (and
      (not (holding_rh ?c ?obj))
      (not (holding_lh ?c ?obj))
      (inside ?obj ?container)
    )
  )

  ;; Switch on an object
  (:action switch_on_object
    :parameters (?c - character ?obj - object)
    :precondition (and
      (switch ?obj)
      (off_state ?obj)
      (close_char_object ?c ?obj)
    )
    :effect (and
      (on_state ?obj)
      (not (off_state ?obj))
    )
  )

  ;; Switch off an object
  (:action switch_off_object
    :parameters (?c - character ?obj - object)
    :precondition (and
      (switch ?obj)
      (on_state ?obj)
      (close_char_object ?c ?obj)
    )
    :effect (and
      (off_state ?obj)
      (not (on_state ?obj))
    )
  )
)
