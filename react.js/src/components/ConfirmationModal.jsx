import React from 'react';
import { Modal, Button } from 'react-bootstrap';

export const ConfirmationModal = ({ show, onClose, onConfirm }) => {
  return (
    <Modal show={show} onHide={onClose} centered>
      <Modal.Header closeButton>
        <Modal.Title>Confirmação</Modal.Title>
      </Modal.Header>
      <Modal.Body>
        Ao prosseguir, você concorda com o armazenamento das informações fornecidas e autoriza o tratamento de seus dados, nos termos da Lei Geral de Proteção de Dados, com a finalidade única e exclusiva de contribuir para melhorias nos materiais publicitários da empresa.
      </Modal.Body>
      <Modal.Footer>
        <Button variant="danger" onClick={onClose}>
          Cancelar
        </Button>
        <Button variant="primary" onClick={onConfirm}>
          Entendi!
        </Button>
      </Modal.Footer>
    </Modal>
  );
};
