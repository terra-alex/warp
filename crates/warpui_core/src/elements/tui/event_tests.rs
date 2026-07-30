use super::*;
use crate::event::{KeyEventDetails, ModifiersState};
use crate::keymap::Keystroke;

#[test]
fn real_input_records_user_activity() {
    let key = TuiEvent::KeyDown {
        keystroke: Keystroke::parse("a").unwrap(),
        chars: "a".to_string(),
        details: KeyEventDetails::default(),
        is_composing: false,
    };
    let paste = TuiEvent::Paste {
        text: "text".to_string(),
    };
    let click = TuiEvent::LeftMouseDown {
        position: TuiPoint::new(1, 1),
        modifiers: ModifiersState::default(),
        click_count: 1,
        is_first_mouse: false,
    };

    assert!(key.records_user_activity());
    assert!(paste.records_user_activity());
    assert!(click.records_user_activity());
}

#[test]
fn movement_and_scrolling_do_not_record_user_activity() {
    let moved = TuiEvent::MouseMoved {
        position: TuiPoint::new(1, 1),
        modifiers: ModifiersState::default(),
        is_synthetic: false,
    };
    let synthetic_moved = TuiEvent::MouseMoved {
        position: TuiPoint::new(1, 1),
        modifiers: ModifiersState::default(),
        is_synthetic: true,
    };
    let scroll = TuiEvent::ScrollWheel {
        position: TuiPoint::new(1, 1),
        delta: (0, 1),
        precise: false,
        modifiers: ModifiersState::default(),
    };

    assert!(!moved.records_user_activity());
    assert!(!synthetic_moved.records_user_activity());
    assert!(!scroll.records_user_activity());
}
